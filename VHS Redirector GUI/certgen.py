import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization import PublicFormat
import subprocess
import datetime

def genCert():
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Create a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "CA"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "British Columbia"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Burnaby"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "VHS:END Project"),
        x509.NameAttribute(NameOID.COMMON_NAME, "example.com"),
    ])
    
    builder = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
    	    x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True
    ).add_extension(
        x509.NameConstraints(
    	permitted_subtrees=[x509.DNSName(".vhsgame.com")],
    	excluded_subtrees=None
        ), critical=False
    )
    certificate = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )
    
    # Save the private key and certificate to the directory
    private_key_path = "VHS_certificate_private_key.pem"
    certificate_path = "VHS_certificate.crt"
    with open(private_key_path, "wb") as private_key_file:
        private_key_file.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        ))

    with open(certificate_path, "wb") as certificate_file:
        certificate_file.write(certificate.public_bytes(Encoding.PEM))

    # Return the private key and certificate paths
    return private_key_path, certificate_path
    
    
