import paramiko

# Specify the file path for the private key
private_key_path = 'key.pem'

# Generate an RSA key pair
key = paramiko.RSAKey.generate(2048)

# Save the private key to a file
key.write_private_key_file(private_key_path)

print(f"Private key generated and saved to {private_key_path}")