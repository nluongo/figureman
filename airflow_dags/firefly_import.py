from airflow.operators.bash_operator import BashOperator

import_task = BashOperator(task_id='firefly_import', bash_command='firefly_import.sh')
