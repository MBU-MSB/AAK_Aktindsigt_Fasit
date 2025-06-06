"""This module contains configuration constants used across the framework"""

# The number of times the robot retries on an error before terminating.
MAX_RETRY_COUNT = 10

# Whether the robot should be marked as failed if MAX_RETRY_COUNT is reached.
FAIL_ROBOT_ON_TOO_MANY_ERRORS = True

# Error screenshot config
SMTP_SERVER = "smtp.aarhuskommune.local"
SMTP_PORT = 25
SCREENSHOT_SENDER = "robot@friend.dk"

# Constant/Credential names
ERROR_EMAIL = "du@msb.aarhus.dk"

# Queue specific configs
# ----------------------

# The name of the job queue (if any)
QUEUE_NAME = '025_01_AAK_Aktindsigt_Fasit'

RESULT_TABLE = '[dbo].[Result_025_01_AAK_Aktindsigt_Fasit]'

# The limit on how many queue elements to process
MAX_TASK_COUNT = 10000

# ----------------------
