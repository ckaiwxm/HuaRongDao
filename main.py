import search
import queue
from queue import PriorityQueue
# Kaiwen Chen
# k2999che
# 20713621
# Reference: I have used build-in library queue for Piority Queue


def a_star(initial_state):
    # Count the number of expanded states and keep a dict of them
    expanded = 0
    expanded_set = set()

    # Store the frontier as Priority Queue
    frontier = PriorityQueue()

    # Start from the initial state
    frontier.put((search.get_total(initial_state), initial_state))

    while(frontier.empty() == False):
        # Select the frontier with minumum total cost
        selected = frontier.get()[1]

        # Pruning
        if(search.state_to_key(selected) in expanded_set):
            continue
        else:
            expanded_set.add(search.state_to_key(selected))
            successors = search.get_successors(selected)

            # Increase ounter
            expanded += 1

            # Put all successors of selected state into frontier
            for scs in successors:
                if(search.is_goal(scs)):
                    return(scs, expanded)
                else:
                    frontier.put((search.get_total(scs), scs))

    return (None, -1, -1)


def dfs(initial_state):
    # Count the number of expanded states and keep a dict of them
    expanded = 0
    expanded_set = set()

    # Store the frontier as Priority Queue
    frontier = []

    # Start from the initial state
    frontier.append(initial_state)
    expanded_set.add(search.state_to_key(initial_state))

    while(len(frontier) != 0):
        # Select the frontier with minumum total cost
        selected = frontier.pop()
        successors = search.get_successors(selected)

        # Increase ounter
        expanded += 1

        # Put all successors of selected state into frontier
        for scs in successors:
            if(search.is_goal(scs)):
                return(scs, expanded)
            #  Cycle pruning
            if(search.state_to_key(scs) not in expanded_set):
                frontier.append(scs)
                expanded_set.add(search.state_to_key(scs))
    return (None, -1, -1)


initial_state = search.read_puzzle(1)
solution = a_star(initial_state)
search.states_to_output(id=1, algo="astar", init_state=initial_state,
                        end_state=solution[0], expanded=solution[1])
solution = dfs(initial_state)
search.states_to_output(id=1, algo="dps", init_state=initial_state,
                        end_state=solution[0], expanded=solution[1])

initial_state = search.read_puzzle(2)
solution = a_star(initial_state)
search.states_to_output(id=2, algo="astar", init_state=initial_state,
                        end_state=solution[0], expanded=solution[1])
solution = dfs(initial_state)
search.states_to_output(id=2, algo="dps", init_state=initial_state,
                        end_state=solution[0], expanded=solution[1])
