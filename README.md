# Automated EBS Snapshot Creation and Cleanup using AWS Lambda & Boto3

## Objective

Automate the creation of EBS snapshots and delete snapshots older than a specified retention period using AWS Lambda and Boto3.

---

## AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EBS
- Amazon EventBridge Scheduler
- AWS IAM
- Amazon CloudWatch Logs

---

## Architecture

EventBridge Scheduler
        |
        v
AWS Lambda (Python 3.12)
        |
        +--> Create EBS Snapshot
        |
        +--> Tag Snapshot
        |
        +--> Find Tagged Snapshots
        |
        +--> Delete Snapshots Older Than 30 Days
        |
        v
CloudWatch Logs

---

## IAM Permissions

The Lambda execution role includes least-privilege permissions:

- ec2:CreateSnapshot
- ec2:DescribeSnapshots
- ec2:DeleteSnapshot
- ec2:CreateTags

Additionally, the managed policy:

- AWSLambdaBasicExecutionRole

was attached to enable CloudWatch logging.

---

## Implementation Steps

1. Created an EC2 instance.
2. Identified the attached EBS Volume ID.
3. Created an IAM Role with least-privilege permissions.
4. Created a Lambda function using Python 3.12.
5. Implemented snapshot creation using Boto3.
6. Tagged snapshots with `CreatedBy=Lambda-Backup`.
7. Listed snapshots using `describe_snapshots()`.
8. Deleted snapshots older than the configured retention period.
9. Configured EventBridge Scheduler to execute weekly.
10. Verified execution using CloudWatch Logs.

---

## Testing

For testing, the retention period was temporarily changed to:

```python
RETENTION_DAYS = 0
```

This verified that the cleanup logic worked correctly.

Before final submission, it was restored to:

```python
RETENTION_DAYS = 30
```

---

## EventBridge Scheduler

Schedule Type:

```
rate(7 days)
```

Runs automatically once every week.

---

## CloudWatch Logs

The logs confirm:

- Snapshot creation
- Snapshot tagging
- Snapshot discovery
- Snapshot deletion (during testing)
- Successful Lambda execution

---

## Discussion

AWS Data Lifecycle Manager (DLM) is the recommended managed solution for standard EBS snapshot scheduling and retention.

AWS Lambda is a better choice when custom logic is required, such as:

- Conditional retention policies
- Custom tagging
- Cross-account snapshot copies
- Notifications through SNS or Slack
- Integration with other AWS services

---

## Cleanup

After testing:

- Terminate the EC2 instance
- Delete unused snapshots
- Delete the EventBridge schedule
- Delete the Lambda function (optional)
- Remove unused IAM resources (optional)

---

## Author

Rajesh Injam