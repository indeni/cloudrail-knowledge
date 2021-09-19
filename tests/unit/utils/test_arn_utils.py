import unittest

from cloudrail.knowledge.utils.arn_utils import are_arns_intersected


class TestArnUtils(unittest.TestCase):

    def test_similar_arn_pass(self):
        # Arrange
        first_arn = 'arn:aws:ec2:us-east-1:115553109071:subnet/subnet-04a600b4600634731'
        second_arn = 'arn:aws:ec2:us-east-1:115553109071:subnet/subnet-04a600b4600634731'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertTrue(result)

    def test_one_valid_arn_one_tf_address_fail(self):
        # Arrange
        first_arn = 'arn:aws:ec2:us-east-1:115553109071:subnet/subnet-04a600b4600634731'
        second_arn = 'aws_subnet.arn'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertFalse(result)

    def test_partial_arn_fail(self):
        # Arrange
        first_arn = '111111111111:function:ServerlessExample'
        second_arn = 'arn:aws:lambda:us-east-1:115553109071:function:ServerlessExample:$LATEST'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertFalse(result)

    def test_arn_with_wildcards_pass(self):
        # Arrange
        first_arn = 'arn:aws:iam::115553109071:user/*'
        second_arn = 'arn:aws:iam::115553109071:user/imanuel'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertTrue(result)

    def test_tf_addresses_arn_pass(self):
        # Arrange
        first_arn = 'aws_lb_target_group.test.arn'
        second_arn = 'aws_lb_target_group.test.arn'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertTrue(result)

    def test_both_wildcards_pass(self):
        # Arrange
        first_arn = '*'
        second_arn = '*'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertTrue(result)

    def test_one_wildcards_pass(self):
        # Arrange
        first_arn = '*'
        second_arn = 'arn:aws:ec2:us-east-1:115553109071:subnet/subnet-04a600b4600634731'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertTrue(result)

    def test_two_unlike_tf_address_fail(self):
        # Arrange
        first_arn = 'aws_lb_target_group.test.arn'
        second_arn = 'aws_iam_role.codebuild.arn'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertFalse(result)

    def test_with_wildcards_s3_bucket_pass(self):
        # Arrange
        first_arn = 'arn:aws:s3:::static-web-resources-bucket-cloudrail-aoi-public-test/*'
        second_arn = 'arn:aws:s3:::static-web-resources-bucket-cloudrail-aoi-public-test'
        # Act
        result = are_arns_intersected(first_arn, second_arn)
        # Assert
        self.assertTrue(result)
