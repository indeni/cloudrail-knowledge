name                = "consoleme"
stage               = "somestage"
namespace           = "sfdc"
region              = "us-east-1"
default_tags        = {}
key_name            = "kinnaird"
vpc_cidr            = "10.1.1.0/24"
public_subnet_cidrs = ["10.1.1.128/28", "10.1.1.144/28"]
subnet_azs          = ["us-east-1a", "us-east-1b"]
private_subnet_cidrs = ["10.1.1.0/28"]
instance_type = "t2.2xlarge"
application_admin   = "y@indeni.com"

allowed_inbound_cidr_blocks = ["0.0.0.0/0"]  // NOTE: Do not open this up to 0.0.0.0/0. Restrict access to your IP address for the demo.
allow_internet_access = true // Set this to true if you want to be able to access the server from the Internet.
bucket_name_prefix = "your-name-prefix"


lb-authentication-authorization-endpoint = "https://accounts.google.com/o/oauth2/auth"
lb-authentication-client-id = "150686249207-t0a8tqjeosi8tnb3aku7d8iiidsejpo7.apps.googleusercontent.com"
lb-authentication-client-secret = "myAz-7Gusb6D75IAGZiWaT2V"
lb-authentication-issuer = "https://accounts.google.com"
lb-authentication-jwt-email-key = "email"
lb-authentication-token-endpoint = "https://oauth2.googleapis.com/token"
lb-authentication-user-info-endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
lb-authentication-scope = "https://www.googleapis.com/auth/admin.directory.group.readonly email openid"