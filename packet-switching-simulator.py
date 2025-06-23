import copy

# This script simulates packet switching in a network.
# The network is modeled as a list of nodes, each with outgoing links and queues for packets.

# Define the network topology as a list of nodes.
# Each node has an 'id' and a list of 'links'.
# Each link has:
#   - 'id': destination node id
#   - 'capacity': link capacity (bits/sec)
#   - 'tau': propagation delay (seconds)
#   - 'queue': list of packets waiting to be transmitted
# Each packet in the queue has:
#   - 'id': unique packet identifier
#   - 'len': packet length (bits)
#   - 'path': list of node ids representing the route
#   - 'arrivalTime': time packet arrived at the current queue
#   - 'departureTime': time packet is scheduled to depart from the queue
main_net = [
    {
        "id": 1,
        "links": [
            {"id": 2, "capacity": 100, "tau": 1, "queue": [
                {"id": "A", "len": 1000, "path": [1, 2, 3], "arrivalTime": 0.0, "departureTime": 0.0},
                {"id": "B", "len": 500, "path": [1, 2, 4], "arrivalTime": 0.0, "departureTime": 0.0}
            ]},
        ]
    },
    {
        "id": 2,
        "links": [
            {"id": 3, "capacity": 100, "tau": 3, "queue": []},
            {"id": 4, "capacity": 1000, "tau": 4, "queue": []}
        ]
    },
    {
        "id": 3,
        "links": []
    }
    ,
    {
        "id": 4,
        "links": []
    }
]

def calc_transfer_time(network, new_network, packet_list):
    """
    Simulates the transfer of packets through the network.
    Updates packet arrival and departure times, moves packets along their paths,
    and marks packets as arrived when they reach their destination.
    """
    # Iterate through each node in the network
    for node in network:
        for link in node['links']:
            # Skip links with empty queues
            if not link['queue']:
                continue

            # Sort the queue by arrival time to process packets in order
            link['queue'].sort(key=lambda x: x['arrivalTime'])

            # Process each packet in the queue
            for i in range(len(link['queue'])):
                packet = link['queue'][i]
                # Remove the current node from the packet's path
                packet['path'].pop(0)
                # If not the first packet, ensure no overlap in transmission
                if i != 0:
                    previous_packet = link['queue'][i - 1]
                    if packet['arrivalTime'] < previous_packet['departureTime']:
                        packet['arrivalTime'] = previous_packet['departureTime']

                # Calculate the time to transfer the packet over the link
                transfer_time = packet['len'] / link['capacity']
                packet['departureTime'] = packet['arrivalTime'] + transfer_time

                # Print packet details after processing
                print(f"Packet ID: {packet['id']}, Arrival Time: {packet['arrivalTime']}, Departure Time: {packet['departureTime']}, Path: {packet['path']}")

                # Update arrival time for the next hop (includes propagation delay)
                packet['arrivalTime'] = packet['departureTime'] + link['tau']

                # If the packet has reached its final destination
                if len(packet['path']) <= 1:
                    print(f"Packet {packet['id']} has reached its final destination in {packet['arrivalTime']} seconds.")
                    # Mark the packet as arrived in the packet list
                    for pack in packet_list:
                        if pack['id'] == packet['id']:
                            pack['arrived'] = True
                else:
                    # Otherwise, move the packet to the next link's queue in the new network
                    new_source = packet['path'][0]
                    new_dest = packet['path'][1]
                    # Find the next link in the new network
                    for new_node in new_network:
                        if new_node['id'] == new_source:
                            for new_link in new_node['links']:
                                if new_link['id'] == new_dest:
                                    # Add the packet to the new link's queue
                                    new_link['queue'].append(packet)
                                    print(f"Packet {packet['id']} transferred to Node {new_dest} at time {packet['arrivalTime']}.")
                                    break
                            break
                print("--------------------------------------------------")

def print_network_info(network):
    """
    Prints the details of the network in a readable format.
    Shows nodes, their links, and the packets in each link's queue.
    """
    for node in network:
        print(f"Node ID: {node['id']}")
        # Check if the node has any links
        if node['links']:
            for link in node['links']:
                print(f"  Link to Node ID: {link['id']}, Capacity: {link['capacity']}, Tau: {link['tau']}")
                # Print queue details if not empty
                if link['queue']:
                    print("  Queue:")
                    for packet in link['queue']:
                        print(f"    Packet ID: {packet['id']}, Length: {packet['len']}, Path: {packet['path']}, Arrival Time: {packet['arrivalTime']}, Departure Time: {packet['departureTime']}")
                else:
                    print("  Queue is empty.")
        else:
            print("  No links connected to this node.")
        print()  # Blank line for readability

if __name__ == "__main__":
    # Print the initial state of the network
    print_network_info(main_net)

    # Prepare a list to track all packets and their arrival status
    packetList = []
    for node in main_net:
        for link in node['links']:
            for packet in link['queue']:
                packet['arrived'] = False  # Add 'arrived' flag to each packet
                packetList.append(packet)

    # Print initial packet information
    print("Initial Packets in the Network:")
    for packet in packetList:
        print(f"Packet ID: {packet['id']}, Length: {packet['len']}, Path: {packet['path']}, Arrival Time: {packet['arrivalTime']}, Departure Time: {packet['departureTime']}, arrived: {packet['arrived']}")

    # Create a deep copy of the network for simulation steps
    new_network = copy.deepcopy(main_net)

    # Main simulation loop: continue until all packets have arrived
    while not all(packet['arrived'] for packet in packetList):
        # Clear all queues in the new network before each step
        for node in new_network:
            for link in node['links']:
                link['queue'].clear()
        # Print the current state of the network
        print_network_info(new_network)

        # Simulate packet transfers for this step
        calc_transfer_time(main_net, new_network, packetList)

        # Update the main network for the next iteration
        main_net = copy.deepcopy(new_network)
        # Print the updated state of the network
        print_network_info(main_net)
        print("--------------------------------------------------")
