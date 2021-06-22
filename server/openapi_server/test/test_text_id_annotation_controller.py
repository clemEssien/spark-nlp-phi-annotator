# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_id_annotation_request import TextIdAnnotationRequest  # noqa: E501
from openapi_server.models.text_id_annotation_response import TextIdAnnotationResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTextIdAnnotationController(BaseTestCase):
    """TextIdAnnotationController integration test stubs"""

    def test_create_text_id_annotations(self):
        """Test case for create_text_id_annotations

        Annotate IDs in a clinical note
        """
        text_id_annotation_request = {
  "note" : {
    "identifier" : "awesome-note",
    "text" : "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott in Seattle. Her SSN is 123-45-6789.\n",
    "type" : "loinc:LP29684-5",
    "patientId" : "awesome-patient"
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/textIdAnnotations',
            method='POST',
            headers=headers,
            data=json.dumps(text_id_annotation_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
