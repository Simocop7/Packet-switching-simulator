# Packet-switching-simulator

This Python project simulates delays in **packet-switched networks**, developed as a practical extension of topics covered in the *Foundations of Communication and the Internet* course (Politecnico di Milano, A.Y. 2024/2025).

## 🧠 Objectives

- Model a network of nodes, links, queues, and packets.
- Compute and trace:
  - **Transmission delay** (`length / capacity`)
  - **Propagation delay** (`tau` parameter)
  - **Queuing delay** (FIFO with arrival/departure dynamics)
- Simulate packet forwarding over multi-hop predefined paths.

## ⚙️ How It Works

The network is represented as a list of nodes, each with:
- **Outgoing links** (with capacity, propagation delay, and packet queues)
- **Packets** (defined by size, path, arrival and departure times)

The simulation loop updates the network iteratively until all packets reach their final destinations, while printing:
- Packet arrival and departure times
- Queue states and transitions
- Dynamic propagation over the network

## ▶️ Run the Script

Requires Python ≥ 3.7. To execute:

```bash
python pack_switching_latest.py
