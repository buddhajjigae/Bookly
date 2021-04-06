import boto3
import uuid


class CommentsTable(object):
    REGION_NAME = "us-east-2"

    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb", region_name=self.REGION_NAME)
        self.table = self.dynamodb.Table("comments")

    def get_all_comments(self):
        response = self.table.scan()
        return response.get("Items", [])

    def get_comment_by_id(self, comment_id):
        key = {"comment_id": comment_id}
        response = self.table.get_item(Key=key)
        return response.get("Item")

    def get_comments_by_user(self, user):
        expression_attributes = {":uvalue": user}
        filter_expression = "user_email= :uvalue"
        return self._scan_and_filter_table(filter_expression, expression_attributes)

    def get_comments_by_tag(self, tag):
        expression_attributes = {":tvalue": tag}
        filter_expression = "contains(tags, :tvalue)"
        return self._scan_and_filter_table(filter_expression, expression_attributes)

    def get_user_comments_by_tag(self, user, tag):
        expression_attributes = {":tvalue": tag, ":uvalue": user}
        filter_expression = "contains(tags, :tvalue) and user_email= :uvalue"
        return self._scan_and_filter_table(filter_expression, expression_attributes)

    def create_comment(self, comment):
        response = self.table.put_item(Item=comment)
        return response

    def update_comment(self, comment_id, new_user, new_text, new_tags, new_version_id):
        old_comment = self.get_comment_by_id(comment_id)
        incoming_version_id = new_version_id
        new_version_id = str(uuid.uuid4())

        new_user = new_user or old_comment["user_email"]
        new_text = new_text or old_comment["comment_text"]
        new_tags = new_tags or old_comment["tags"]

        key = {"comment_id": comment_id}
        conditional_expression = "version_id = :incoming_version_id"
        update_expression = "SET version_id = :new_version_id, user_email = :new_user, comment_text = :new_text, tags = :new_tags"
        expression_values = {
            ":incoming_version_id": incoming_version_id,
            ":new_user": new_user,
            ":new_text": new_text,
            ":new_tags": new_tags,
            ":new_version_id": new_version_id,
        }

        try:
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ConditionExpression=conditional_expression,
                ExpressionAttributeValues=expression_values,
            )
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException as ex:
            msg = "Failed to update {}! {}".format(comment_id, ex)
            response = {"ResponseMetadata": {"ResponseMsg": msg, "HTTPStatusCode": 400}}
            return response

        msg = "Updated {}".format(comment_id)
        response.setdefault("ResponseMetadata", {})["ResponseMsg"] = msg
        return response

    def add_response_to_comment(self, comment_id, response):
        key = {"comment_id": comment_id}
        update_expression = "SET responses = list_append(responses, :i)"
        expression_attribute_values = {":i": [response]}
        return_values = "UPDATED_NEW"

        res = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues=return_values,
        )

        return res

    def _scan_and_filter_table(self, filter_expression, expression_attributes):
        result = self.table.scan(
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attributes,
        )
        return result.get("Items", [])
