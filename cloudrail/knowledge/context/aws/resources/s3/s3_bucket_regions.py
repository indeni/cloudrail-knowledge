class S3BucketRegions:

    def __init__(self, bucket_name: str, region: str):
        self.bucket_name: str = bucket_name
        self.bucket_region: str = region
