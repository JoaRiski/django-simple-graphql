import json


class GraphQLClient:
    GRAPHQL_URL = "/graphql"

    def __init__(self, client):
        self.client = client

    def query(
        self,
        query,
        op_name=None,
        input_data=None,
        variables=None,
    ):
        body = {"query": query}
        if op_name:
            body["operation_name"] = op_name
        if variables:
            body["variables"] = variables
        if input_data:
            if variables in body:
                body["variables"]["input"] = input_data
            else:
                body["variables"] = {"input": input_data}
        resp = self.client.post(
            self.GRAPHQL_URL, json.dumps(body), content_type="application/json"
        )
        return resp

    def assert_response_has_no_errors(self, resp):
        assert resp.status_code == 200
        content = json.loads(resp.content)
        assert "errors" not in list(content.keys())

    def assert_response_has_errors(self, resp):
        content = json.loads(resp.content)
        assert "errors" in list(content.keys())

    def assert_response_has_error_message(self, response, message):
        content = json.loads(response.content)
        assert "errors" in content
        errors = json.dumps(content["errors"])
        assert message in errors, f"{message} not found in {errors}"

    def get_single_query_result(self, response):
        content = json.loads(response.content)
        data = content["data"]
        return data[next(iter(data.keys()))]

    def assert_first_result_matches_expected(self, response, expected):
        result = self.get_single_query_result(response)
        assert len(expected) == len(result), f"{len(expected)} == {len(result)}"
        for key, value in expected.items():
            assert key in result, f"{result}"
            assert result[key] == value, f"{result[key]} == {value}"

    def ensure_set(self, data):
        multiple = hasattr(data, "__iter__") and not isinstance(
            data, (str, bytes, bytearray)
        )
        if not multiple:
            return {data}
        else:
            return set(data)

    def get_node_ids(self, response) -> set:
        data = self.get_single_query_result(response)

        if "edges" in data:
            edges = data["edges"]
            result = set()
            for edge in edges:
                result.add(edge["node"]["id"])
            return result
        else:
            return {data["id"]}

    def assert_query_result_node_ids_match(self, response, expected):
        response_ids = self.get_node_ids(response)
        expected_ids = self.ensure_set(expected)

        assert len(response_ids) == len(expected_ids)
        for entry in expected_ids:
            assert entry in response_ids
            response_ids.remove(entry)

    def assert_query_result_has_no_ids(self, response, unexpected):
        unexpected_ids = self.ensure_set(unexpected)
        response_ids = self.get_node_ids(response)
        for entry in unexpected_ids:
            assert entry not in response_ids

    def assert_query_result_link_node_ids_match(self, response, link, expected):
        expected_ids = self.ensure_set(expected)

        data = self.get_single_query_result(response)
        link_data = data[link]["edges"]
        assert len(expected_ids) == len(link_data)
        for edge in link_data:
            assert edge["node"]["id"] in expected_ids
            expected_ids.remove(edge["node"]["id"])

    def assert_query_result_is_empty(self, response):
        data = self.get_single_query_result(response)
        if data:
            assert len(data["edges"]) == 0
        else:
            assert data is None
