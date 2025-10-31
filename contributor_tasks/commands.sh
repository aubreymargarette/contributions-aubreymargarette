uv run tb run --agent oracle --task-id template-task --dataset-path contributor_tasks

uv run tb run --agent nop --task-id template-task --dataset-path contributor_tasks


uv run tb run --agent terminus-2 --model openrouter/openai/gpt-oss-120b --task-id template-task --dataset-path contributor_tasks --n-attempts 5

uv run tb run --agent terminus-2 --model openrouter/openai/gpt-5 --task-id template-task --dataset-path contributor_tasks --n-attempts 3


uv run tb tasks check template-task --model openrouter/openai/gpt-5 --tasks-dir contributor_tasks
