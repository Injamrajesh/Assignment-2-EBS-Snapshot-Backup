import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client("ec2")

VOLUME_ID = "vol-06e5bdd5e690deb8c"
RETENTION_DAYS = 30

def lambda_handler(event, context):
    print("Lambda function started")

    # Create snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated backup created by Lambda"
    )

    print(f"Snapshot created: {snapshot['SnapshotId']}")

    # Tag snapshot
    ec2.create_tags(
        Resources=[snapshot["SnapshotId"]],
        Tags=[
            {
                "Key": "CreatedBy",
                "Value": "Lambda-Backup"
            }
        ]
    )

    print("Tag added successfully")

    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    # Get snapshots created by Lambda
    snapshots = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {
                "Name": "tag:CreatedBy",
                "Values": ["Lambda-Backup"]
            }
        ]
    )

    print(f"Found {len(snapshots['Snapshots'])} tagged snapshot(s)")

    # Check each snapshot
    for snap in snapshots["Snapshots"]:
        snapshot_id = snap["SnapshotId"]
        start_time = snap["StartTime"]

        print(f"Checking snapshot: {snapshot_id}")

        if start_time < cutoff_date:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot: {snapshot_id}")
        else:
            print(f"Keeping snapshot: {snapshot_id}")

    return {
        "statusCode": 200,
        "body": f"Snapshot {snapshot['SnapshotId']} created successfully."
    }