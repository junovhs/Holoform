#!/usr/bin/env python3
"""
Script to update all tasks in Milestone 6 to include status: "todo"
"""

import re

def update_tasks_status():
    # Read the tasks.yaml file
    with open('tasks.yaml', 'r') as f:
        content = f.read()
    
    # Find the milestone_6 section
    milestone_6_match = re.search(r'milestone_6:(.*?)(?=milestone_\d+:|$)', content, re.DOTALL)
    if not milestone_6_match:
        print("Milestone 6 section not found")
        return
    
    milestone_6_content = milestone_6_match.group(0)
    
    # Find all task entries that don't have a status field
    task_pattern = re.compile(r'(- id: M6\.\d+\.\d+\.\d+\n.*?deliverable: ".*?")', re.DOTALL)
    
    def add_status(match):
        task_text = match.group(1)
        if "status:" not in task_text:
            return task_text + '\n          status: "todo"'
        return task_text
    
    updated_milestone_6 = task_pattern.sub(add_status, milestone_6_content)
    
    # Replace the milestone_6 section in the original content
    updated_content = content.replace(milestone_6_content, updated_milestone_6)
    
    # Write the updated content back to the file
    with open('tasks.yaml', 'w') as f:
        f.write(updated_content)
    
    print("Updated all tasks in Milestone 6 to include status: 'todo'")

if __name__ == "__main__":
    update_tasks_status()