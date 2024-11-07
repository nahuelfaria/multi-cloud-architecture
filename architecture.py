from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.security import IAM, KMS
from diagrams.azure.compute import CloudsimpleVirtualMachines
from diagrams.azure.network import LoadBalancers, DNSPrivateZones
from diagrams.azure.database import SQLDatabases, CosmosDb
from diagrams.azure.storage import BlobStorage
from diagrams.gcp.compute import GCE, GKE
from diagrams.gcp.network import LoadBalancing, DNS as GCP_DNS
from diagrams.gcp.database import SQL, BigTable
from diagrams.gcp.storage import GCS

with Diagram("Arquitectura Multi-Cloud", show=False):
    aws_dns = Route53("AWS DNS")
    azure_dns = DNSPrivateZones("Azure DNS")
    gcp_dns = GCP_DNS("GCP DNS")

    aws_lb = ELB("AWS Load Balancer")
    azure_lb = LoadBalancers("Azure Load Balancer")
    gcp_lb = LoadBalancing("GCP Load Balancer")

    with Cluster("AWS"):
        aws_web1 = EC2("Web Server 1")
        aws_web2 = EC2("Web Server 2")

        with Cluster("Database Cluster"):
            aws_rds = RDS("RDS")
            aws_dynamo = Dynamodb("DynamoDB")

        aws_s3 = S3("S3 Storage")
        aws_sqs = SQS("SQS Queue")
        aws_sns = SNS("SNS Notifications")

    with Cluster("Azure"):
        azure_vm1 = CloudsimpleVirtualMachines("VM 1")
        azure_vm2 = CloudsimpleVirtualMachines("VM 2")

        with Cluster("Database Cluster"):
            azure_sql = SQLDatabases("SQL Database")
            azure_cosmos = CosmosDb("CosmosDB")

        azure_blob = BlobStorage("Blob Storage")

    with Cluster("GCP"):
        gcp_vm1 = GCE("VM 1")
        gcp_vm2 = GCE("VM 2")
        gcp_gke = GKE("GKE Cluster")

        with Cluster("Database Cluster"):
            gcp_sql = SQL("SQL Database")
            gcp_bigtable = BigTable("BigTable")

        gcp_gcs = GCS("GCS Storage")


    aws_dns >> aws_lb
    azure_dns >> azure_lb
    gcp_dns >> gcp_lb

    aws_lb >> [aws_web1, aws_web2]
    azure_lb >> [azure_vm1, azure_vm2]
    gcp_lb >> [gcp_vm1, gcp_vm2]

    aws_web1 >> aws_rds
    aws_web2 >> aws_dynamo

    azure_vm1 >> azure_sql
    azure_vm2 >> azure_cosmos

    gcp_vm1 >> gcp_sql
    gcp_vm2 >> gcp_bigtable

    aws_web1 >> aws_s3
    aws_web2 >> aws_s3

    azure_vm1 >> azure_blob
    azure_vm2 >> azure_blob

    gcp_gke >> gcp_gcs

    aws_sqs >> aws_sns
    gcp_gcs >> gcp_gke

    aws_rds >> KMS("KMS")
    aws_dynamo >> IAM("IAM")

    azure_sql >> IAM("IAM")
    azure_cosmos >> IAM("IAM")
    