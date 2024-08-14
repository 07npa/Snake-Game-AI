# COSC550 - Assignment 1 - Student's Report

## Phuong Anh Nguyen - Student ID: 220276190

## Class of the Agent Program

**Model-Based Agents**: These agents maintain an internal state to make decisions. This technique aligns well with our need to track and avoid body and obstacle locations and to ensure the agent doesn't move in the opposite direction.

This technique was chosen because it provides a balance between simplicity and efficiency, allowing the agent to use past and present information to make decisions. In our implementation, the agent uses an internal representation **(environment_map)** to track locations marked as **body ('B')**, **obstacles ('O')**, and **food ('F')**. This model allows the agent to make informed decisions about valid directions.
The function **is_valid_direction** leverages this internal model to decide the validity of the next move, ensuring the agent's actions are based on its perception and memory of the environment.

## AI Techniques Considered

The **A Star Search Algorithm** was selected to find the path to the food. This decision was driven by the algorithm's ability to efficiently find the shortest path in a weighted graph. The **algorithm** uses a combination of the actual cost from the start node to the current node (g) and a heuristic cost estimate from the current node to the goal (h). For the heuristic, I used the **Manhattan distance**, which is appropriate given the grid-based nature of the environment and the goal of the task.

## Reflections

**Challenges encounters:**

**1. Determining Valid Directions:**
- **Challenge**: Ensuring that the agent's decisions about valid directions were accurate and efficient; always find out the valid direction.
- **Solution**: I broke down the conditions into three clear checks (body, obstacles, opposite directions) within the **is_valid_direction** function, and then get it in while loop, it keep looping through four directions until the valid one is found.

**2. Maintaining an Accurate Internal Model**

- **Challenge**: Keeping the internal model **(environment_map)** up-to-date with changes in the environment **(food location, body location)**.
- **Solution**: I ensured that the internal model was updated consistently based on new perceptions, allowing the agent to make informed decisions, using **update_body, update_food** function.