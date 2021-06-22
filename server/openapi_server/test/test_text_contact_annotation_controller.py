# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_contact_annotation_request import TextContactAnnotationRequest  # noqa: E501
from openapi_server.models.text_contact_annotation_response import TextContactAnnotationResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTextContactAnnotationController(BaseTestCase):
    """TextContactAnnotationController integration test stubs"""

    def test_create_text_contact_annotations(self):
        """Test case for create_text_contact_annotations

        Annotate contact information in a clinical note
        """
        text_contact_annotation_request = {
  "note" : {
    "identifier" : "awesome-note",
    "text" : "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott in Seattle. Her phone number is 203-555-4545.\n",
    "type" : "loinc:LP29684-5",
    "patientId" : "awesome-patient"
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/textContactAnnotations',
            method='POST',
            headers=headers,
            data=json.dumps(text_contact_annotation_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
