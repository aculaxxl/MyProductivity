
1. Get all statuses, not repeating, alphabetically ordered
```sql
SELECT DISTINCT is_done 
FROM tasks_task 
ORDER BY is_done ASC;
```

2. get the count of all tasks in each project, order by tasks count descending
```sql
SELECT p.name, COUNT(t.id) as tasks_count 
FROM tasks_project p 
LEFT JOIN tasks_task t ON p.id = t.project_id 
GROUP BY p.id, p.name 
ORDER BY tasks_count DESC;
```

3. get the count of all tasks in each project, order by projects names
```sql
SELECT p.name, COUNT(t.id) as tasks_count
FROM tasks_project p 
LEFT JOIN tasks_task t ON p.id = t.project_id 
GROUP BY p.id, p.name 
ORDER BY LOWER(p.name);
```

4. get the tasks for all projects having the name beginning with "N" letter
```sql
SELECT p.name AS project_name, t.name AS task_name
FROM tasks_project p 
LEFT JOIN tasks_task t ON p.id = t.project_id 
WHERE p.name ILIKE 'N%';
```

5. get the list of al projects containing the 'a' letter in the middle of the name, and show the tasks count near each project. Mention that there can exist projects without tasks and tasks with project_id= NULL
```sql
SELECT COALESCE(p.name, 'No Project') AS project_name, COUNT(t.id) as tasks_count 
FROM tasks_project p
FULL OUTER JOIN tasks_task t ON p.id = t.project_id 
WHERE p.name ILIKE '_%a%_' OR p.name IS NULL
GROUP BY p.id, p.name;
```
6. get the list of tasks with duplicate names. Order alphabetically
```sql
SELECT name, COUNT(id) AS count
FROM tasks_task 
GROUP BY name 
HAVING COUNT(id) > 1 
ORDER BY name ASC;
```

7. get the list of tasks having several exact matches of both name and status, from the project Delivery (in my case 1). Order by matches count
```sql
SELECT t.name AS task_name, t.is_done, COUNT(*) as matches_count
FROM tasks_task t
JOIN tasks_project p ON t.project_id = p.id
WHERE p.name = '1'
GROUP BY t.name, t.is_done
HAVING COUNT(*) > 1
ORDER BY matches_count ASC;
```

8. get the list of project names having more than 10 tasks in status 'completed'. Order by project_id
```sql
SELECT p.name AS project_name, COUNT(t.id) AS completed_tasks_count
FROM tasks_project p
JOIN tasks_task t ON p.id = t.project_id
WHERE t.is_done = TRUE
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id;
```