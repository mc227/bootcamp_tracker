"""
Pivot — Sep 2026 Study Tracker
A tkinter desktop app tracking the curated 26-item O'Reilly playlist
(10 Maxwell/Prasad/Gaines Python courses -> Linux Net/Sec -> Protobuf ->
Sockets -> Bash -> Docker -> Microservices -> System Design -> two coding-
interview courses -> Heineman DSA -> Sarda DSA/Blind75 -> Computer
Architecture -> JavaScript -> CSS -> two interview-strategy courses).

Saves progress to pivot_progress.json in the same folder as this script.
Run it with: python pivot_tracker.py

Rename the app: just change APP_NAME below.
"""

import json
import tkinter as tk
from pathlib import Path
from datetime import date
from tkinter import ttk, messagebox

APP_NAME = "Pivot"          # <- change this to rename the app
TARGET_DEFAULT = "2026-09-30"   # your pivot deadline

# ----------------------------------------------------------------------
# Curriculum — section name + list of items in order.
# Sections are prefixed with the playlist item number (1-26).
# ----------------------------------------------------------------------
CURRICULUM = [
    # ===================== Python craft foundations (Maxwell x8 + Prasad + Gaines) =====================
    ('1 · Pythonic OOP (Maxwell)', [
        'The Key Ideas of Powerful Objects', 'Writing Simple (and Useful) Python Classes',
        "Leveraging Methods (Python's special requirements)",
        'Encapsulation and Data Hiding', "Inheritance and 'is-a' Relationships",
        'The Different Kinds of Inheritance Hierarchies',
        'Interfaces and Abstract Methods',
        'The Single-Responsibility and Substitution Principles',
        'Gracefully Refactoring Your Classes as Requirements Evolve',
        'Python Data Classes', 'Wrap-up and Q&A',
    ]),
    ('2 · Python: Beyond the Basics (Maxwell)', [
        'Generators for Efficient, Scalable, Well-Encapsulated Code',
        "Demystifying Python's Iterator Protocol",
        'Understanding Views, Iterators, and Iterables',
        'Patterns for Scalable Composability',
        'List Comprehensions for Expressive List Creation',
        'Comprehensions of Dicts, Sets, and More',
        'Rich and Expressive Data Structures, Part 2', 'Generator Expressions',
        "Quick Review of Python's Object Syntax",
        'Properties for Clean Design and Refactoring', 'Special Methods',
        'The Factory Pattern', 'The Observer Pattern',
        'How OOP in Python Is Fundamentally Different from Other Languages',
    ]),
    ('3 · Python: The Next Level (Maxwell)', [
        'Variable-Argument Functions', 'Leveraging Argument Unpacking',
        'Understanding Function Objects in Python', 'Using Key Functions',
        'Writing Code That Takes Functions as Arguments',
        'The Amazing Benefits of Decorators', 'Basic Structure of the Decorator',
        'Common Decorator Patterns and Best Practices',
        'Quick Review of Key Decorator Patterns', 'Decorators Taking Arguments',
        'Class-Based Decorators', 'Magic Methods for Custom Syntax and Natural Semantics',
        'Custom Container Classes', 'Iterable Sequence Containers', 'Index and Key Access',
    ]),
    ('4 · Beyond Python Scripts — Logging, Modules & Dependencies (Maxwell)', [
        "Python's Logging System", 'Logging Design Patterns', 'Module Organization',
        'Evolving Reusable Python Modules as Requirements Change', 'Dependency Management',
    ]),
    ('5 · Beyond Python Scripts — Exceptions, Error Handling & CLIs (Maxwell)', [
        "Python's Exception Model", 'Exception Patterns and Anti-patterns',
        'The Most Diabolical Python Anti-pattern (and How to Avoid It)',
        'Building Command-Line Programs', 'Bonus: Advanced Collection Types',
    ]),
    ('6 · Pythonic Design Patterns (Maxwell)', [
        "Python's Object Syntax", 'Overview of Python Object Model Special Features',
        'Properties for Clean Design and Refactoring', 'Special Methods',
        'How OOP in Python Is Fundamentally Different from Other Languages',
        'The Observer Pattern', 'The Factory Patterns',
    ]),
    ('7 · Test-Driven Development in Python (Maxwell)', [
        'Why Writing Tests Is a Superpower', 'The Different Kinds of Automated Tests',
        'Testing Frameworks: The unittest Module', 'Unit Tests and Simple Assertions',
        'Lab: The Text Body', 'Test Organization', 'Fixtures and Common Test Setup',
        'Asserting Exceptions', 'Subtests for Parameterized Tests',
        'Lab: More Advanced Testing', 'Mocks for Rapid Indirect Testing',
        'Tooling for Test Automation', 'The Popular Pytest Framework',
    ]),
    ('8 · Scaling Python with Generators (Maxwell)', [
        'Pythonic Scalability Overview',
        'Generators for Efficient, Scalable, Well-Encapsulated Code',
        "Demystifying Python's Iterator Protocol",
        'Understanding Views, Iterators, and Iterables',
        'Patterns for Scalable Composability',
        'Rich and Expressive Data Structures Overview', 'List Comprehensions',
        'Comprehensions of Dicts, Sets, and More', 'Generator Comprehensions',
    ]),
    ('9 · Concurrency in Python (Prasad)', [
        'Python Thread Overview (GIL, kernel threads, CPython internals, nonblocking I/O, C extensions)',
        'Locks and Semaphores', 'Queues — Share Memory by Communicating',
        'Multiprocessing — Concurrency and Parallelism',
        'Coroutines — Concurrency from Scratch', 'Gevent — Greenlets and Monkey Patching',
        'AsyncIO — async/await, Event Loops, Concurrent Futures',
        'Hacks — A Grab-bag of Async Ideas',
    ]),
    ('10 · Threading in Python (Gaines)', [
        'What Is a Thread?', 'Build a Single-Threaded Application',
        'Build a Simple Multithreaded Application', 'Daemon Threads',
        'Convert a Multithreaded App to Use Daemon Threads', 'Joining Threads (.join())',
        'Create, Start, and Join Multiple Threads Using a Loop', 'ThreadPoolExecutor',
        'Race Conditions', 'Thread Synchronization Using Locks (deadlock)',
        'Wrap-up and Q&A',
    ]),
    # ===================== Linux / domain (Prowse) =====================
    ('11 · Linux Networking & Security (Prowse) — Day 1: Networking', [
        'Network commands & configuration (ip, ss, nmap, tcpdump, nmcli)',
        'Connecting between hosts (SSH keys, certificates, rsync)',
        'Monitoring hosts remotely (rsyslog, Prometheus)',
        'Docker networking (bridges, custom networks, port mapping)',
    ]),
    ('11 · Linux Networking & Security (Prowse) — Day 2: Security', [
        'Linux hardening (services, secure files, intrusion prevention, auditd)',
        'SSH security (port forwarding, 2FA, brute-force protection, key management)',
        'User & application security (authentication, AppArmor, SELinux)',
        'Firewalling (firewalld, nftables)',
    ]),
    # ===================== Protocol / networking domain =====================
    ('12 · Protocol Buffers 3 (Maarek)', [
        'The Need for Protocol Buffers', 'How Are Protocol Buffers Used?',
        'Course Structure', 'First Message', 'Scalar Types', 'Tags', 'Repeated Fields',
        'Comments', 'Default Values for Fields', 'Enumerations (Enums)',
        'Solution to Practice Exercises I', 'Defining Multiple Messages in the Same File',
        'Nesting Messages', 'Imports', 'Packages', 'Solution to Practice Exercises II',
        'Use protoc to Generate Code in Any Language',
        'The Need for Updating the Protocol', 'Rules for Data Evolution', 'Adding Fields',
        'Renaming Fields', 'Removing Fields', 'Reserved Keyword', 'Beware of Defaults',
        'Evolving Enum Fields', 'Integer Types Deep Dive',
        'Advanced Data Types (oneof, map, Timestamp, Duration)',
        'Protocol Buffers Options', 'Naming Conventions', 'Services',
        'Introduction to gRPC', 'Protocol Buffers Internals',
        "What's Next & Congratulations!",
    ]),
    # NOTE: the two hands-on sections below are a topic-level reconstruction of the
    # course's Java and Go code-generation flow — not verbatim video titles.
    # Paste the course's Java/Go outline if you want these made exact.
    ('12 · Protocol Buffers 3 (Maarek) — Hands-on: Java', [
        'Java Project Setup (Gradle + protobuf-gradle-plugin)',
        'Generating Java Code from .proto',
        'Creating a Simple Message in Java',
        'Complex Message (nested, repeated, enums)',
        'Serializing to Bytes & Writing to a File',
        'Reading from a File & Deserializing',
        'Protobuf <-> JSON in Java',
        'Wrap-up (Java)',
    ]),
    ('12 · Protocol Buffers 3 (Maarek) — Hands-on: Go', [
        'Go Project Setup',
        'Installing the Go Plugin (protoc-gen-go)',
        'Generating Go Code from .proto',
        'Creating a Simple Message in Go',
        'Complex Message (nested, repeated, enums)',
        'Writing to a File & Reading Back',
        'Protobuf <-> JSON in Go',
        'Wrap-up (Go)',
    ]),
    ('13 · Python Sockets (Eramo) — Setup & Networking', [
        'Course Preview', 'Python Installation and Setup', 'VS Code Installation',
        'Creating our Working Directory', 'A Brief Overview of Networking Concepts',
    ]),
    ('13 · Python Sockets (Eramo) — TCP & UDP', [
        'Creating a TCP Server Socket', 'Creating a TCP Client Socket',
        'Sending Data through a TCP Connection',
        'Creating and Sending Data through a UDP Server/Client',
        'Exploring the Buffer Size',
    ]),
    ('13 · Python Sockets (Eramo) — Threading Basics', [
        'The Threading Module Basics Pt 1', 'The Threading Module Basics Pt 2',
    ]),
    ('13 · Python Sockets (Eramo) — Serialization (Pickle/JSON)', [
        'The Pickle Module — Sending Objects through the Data Stream',
        'The JSON Module — Sending Objects through the Data Stream',
    ]),
    ('13 · Python Sockets (Eramo) — Fixed-Length Headers', [
        'Fixed-Length Headers — Shortcomings of a Fixed Max Byte Size',
        'Fixed-Length Headers — The Solution',
    ]),
    ('13 · Python Sockets (Eramo) — Basic Two-Way Chat', [
        'Basic Two-Way Chat Pt 1 — Server/Client Setup',
        'Basic Two-Way Chat Pt 2 — Enabling the Chat',
    ]),
    ('13 · Python Sockets (Eramo) — Terminal Chat Room', [
        'Terminal Chat Room Pt 1 — Server/Client Setup',
        'Terminal Chat Room Pt 2 — Adding Functionality',
        'Terminal Chat Room Pt 3 — Adding Functionality',
        'Terminal Chat Room Pt 4 — Functionality & Testing',
    ]),
    ('13 · Python Sockets (Eramo) — Tkinter Module', [
        'Tkinter — Defining a Root Window', 'Tkinter — Adding Frames',
        'Tkinter — Adding Widgets', 'Tkinter — Adding Functionality',
    ]),
    ('13 · Python Sockets (Eramo) — Basic GUI Chat Room', [
        'Basic GUI Chat Pt 1 — Client Layout', 'Basic GUI Chat Pt 2 — Client Layout',
        'Basic GUI Chat Pt 3 — Adding Functionality',
        'Basic GUI Chat Pt 4 — Functionality & Testing',
    ]),
    ('13 · Python Sockets (Eramo) — Advanced GUI Chat Room', [
        'Adv GUI Chat Pt 1 — Updating Client Layout',
        'Adv GUI Chat Pt 2 — Building Server Layout',
        'Adv GUI Chat Pt 3 — Outlining Server Functionality',
        'Adv GUI Chat Pt 4 — Outlining Client Functionality',
        'Adv GUI Chat Pt 5 — Starting the Server',
        'Adv GUI Chat Pt 6 — Processing Messages Server Side',
        'Adv GUI Chat Pt 7 — Starting the Client',
        'Adv GUI Chat Pt 8 — Sending Data Client to Server',
        'Adv GUI Chat Pt 9 — Adding Admin Functionality',
        'Adv GUI Chat Pt 10 — Adding Admin Functionality',
        'Adv GUI Chat Pt 11 — Final Testing',
    ]),
    ('13 · Python Sockets (Eramo) — WAN / Network Config', [
        'Adjusting Host Firewall for LAN Communication',
        'Setting a Static IP Address for WAN Communication',
        'Enabling Port Forwarding for WAN Communication', 'Testing out WAN Communication',
        'Configuring a Second Router (Different Settings)',
    ]),
    ('13 · Python Sockets (Eramo) — Pygame Module', [
        'Pygame — Creating a Game Window and Game Loop',
        'Pygame — Setting Up a Game Class', 'Pygame — Setting Up a Player Class',
    ]),
    ('13 · Python Sockets (Eramo) — Online Multiplayer Game', [
        'Online MP Game Pt 1 — Setting Up the Server',
        'Online MP Game Pt 2 — Setting Up the Client',
        'Online MP Game Pt 3 — Sending Pygame Configs to the Client',
        'Online MP Game Pt 4 — Creating a Player on the Server',
        'Online MP Game Pt 5 — Sending the Player to the Client',
        'Online MP Game Pt 6 — Starting the Game on the Server',
        'Online MP Game Pt 7 — Starting the Game on All Clients',
        'Online MP Game Pt 8 — Player Movement on the Client',
        'Online MP Game Pt 9 — Creating a Game State on the Server',
        'Online MP Game Pt 10 — Processing Game State on All Clients',
        'Online MP Game Pt 11 — Resetting the Game for More Rounds',
        'Online MP Game Pt 12 — Official Network Playtest!',
    ]),
    # ===================== Shell / containers / microservices =====================
    ('14 · Bash Shell Scripting (van Vugt)', [
        'Introducing the sample shell script (flow & elements)',
        'Writing a script with basic elements (readable scripts, internal/external commands)',
        'Working with variables (here-docs, sourcing, read)',
        'Using positional parameters (shift, $*, $@)',
        'Pattern-matching substitution (tr, awk, sed)',
        'Conditional structures (if/then/else, &&/||, while/until, for/case)',
    ]),
    ('15 · Docker for Developers 2026 — Microservices Workshop (Kocherhin)', [
        'Introduction', 'Why Do You Need Docker?', 'Planning Docker Application',
        'Installing Docker Tools', 'Creating Dockerfile', 'Creating API Application',
        'Preparing API Docker Image', 'Starting API Server', 'Docker Hub',
        'Environment Variables', 'Adding Database', 'Making Database Requests', 'Volumes',
        'Auth Service', 'Frontend Service', 'Running Frontend in Production',
        'Docker Exec', 'Setting Up Nginx', 'Proxying API Requests', 'Docker Network',
        'Frontend Proxy', 'Last Tuning', 'Do It Yourself: Mailer Service',
    ]),
    ('16 · Microservices Bootcamp (Newman)', [
        'What Microservices Are', 'The Problem with Coupling', 'Domain-Driven Design',
        'Boundaries, Teamwork & Communication Patterns',
        'Deployment, Troubleshooting, Observability',
    ]),
    # ===================== Interview / CS core =====================
    ('17 · System Design Interview Boot Camp (Bhardwaj)', [
        'System Design Basics', 'Architecture Basics',
        'Mock: Taxi / Streaming / Real-Time Analytics',
        'Mock: News Feed / URL Shortener / Auction', 'Mock: Shopping / Booking / Coupon',
        'Mock: Chat / Taxi / Recommendations', 'Mock: Fraud / Sentiment / Product Search',
        'Challenges, Questions & Tips',
    ]),
    ('18 · Coding Interview Bootcamp (Bhardwaj)', [
        'Coding design framework (7-step)',
        'Sorting, hashing & arrays (two pointers, sliding window)',
        'Search, sorting, stack & priority queue (binary search, BST, heaps)',
        'Graphs, cycle detection & shortest path (BFS/DFS, word ladder)',
        'DAG, scheduling & minimum spanning tree (topological sort, Kruskal/Prim)',
        'Pattern search & majority vote (Dijkstra, DP, KMP/Boyer-Moore, knapsack, greedy)',
    ]),
    ('19 · Algorithms for the Coding Interview (Horstmann)', [
        'The Mastery Learning concept', 'Basic array algorithms (sum, max, min, matches)',
        'Searching (linear, binary)', 'Sorting (selection, merge)',
        'Linked lists (insertion, traversal, deletion)',
        'Hashing (separate chaining, open addressing)',
        'Binary search trees (insertion, deletion, traversal)',
        'Graphs (breadth-first search, Dijkstra)',
    ]),
    ('20 · Intro to Algorithms & Data Structures (Heineman)', [
        'log(n) behavior / Binary Array Search',
        'Basic Data Structures (queue, stack, deque, bag, symbol table, heap, graph)',
        'Sorting (TimSort, InsertionSort, MergeSort)', 'Graph Algorithms',
        'Skip List Implementation',
    ]),
    # ===================== Sarda DSA / Blind 75+ (replaces old Blind 75 section) =====================
    # Confirmed against the full course outline (83 problems + Bonus). The course
    # is a flat problem list; the topic sub-headers below are ours for navigation.
    ('21 · Master DSA / Blind 75+ (Sarda) — Arrays & Hashing', [
        'Two Sum (1)', 'Contains Duplicate (217)', 'Valid Anagram (242)',
        'Group Anagrams (49)', 'Top K Frequent Elements (347)', 'Is Subsequence (392)',
        'Longest Consecutive Sequence (128)', 'Product of Array Except Self (238)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Two Pointers', [
        'Valid Palindrome (125)', 'Two Sum II (167)', '3Sum (15)',
        'Container With Most Water (11)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Sliding Window', [
        'Maximum Average Subarray I (643)', 'Best Time to Buy and Sell Stock (121)',
        'Longest Repeating Character Replacement (424)',
        'Longest Substring Without Repeating Characters (3)',
        'Minimum Window Substring (76)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Linked List', [
        'Middle of the Linked List (876)', 'Linked List Cycle (141)',
        'Linked List Cycle II (142)', 'Reverse Linked List (206)', 'Reorder List (143)',
        'Remove Nth Node From End of List (19)', 'Merge Two Sorted Lists (21)',
        'Merge k Sorted Lists (23)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Stack', [
        'Valid Parentheses (20)', 'Daily Temperatures (739)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Binary Search', [
        'Binary Search (704)', 'Find Minimum in Rotated Sorted Array (153)',
        'Search in Rotated Sorted Array (33)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Trees (DFS/BFS)', [
        'Invert Binary Tree (226)', 'Maximum Depth of Binary Tree (104)',
        'Same Tree (100)', 'Subtree of Another Tree (572)',
        'Lowest Common Ancestor of a BST (235)', 'Binary Tree Level Order Traversal (102)',
        'Validate Binary Search Tree (98)', 'Kth Smallest Element in a BST (230)',
        'Construct Binary Tree from Preorder and Inorder (105)',
        'Binary Tree Maximum Path Sum (124)',
        'Serialize and Deserialize Binary Tree (297)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Backtracking', [
        'Combination Sum (39)', 'Word Search (79)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Tries', [
        'Implement Trie (208)', 'Add and Search Words Data Structure (211)',
        'Word Search II (212)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Heap / Priority Queue', [
        'Find Median from Data Stream (295)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Graphs', [
        'Number of Islands (200)', 'Clone Graph (133)',
        'Pacific Atlantic Water Flow (417)', 'Graph Valid Tree (261)',
        'Number of Connected Components (323)', 'Course Schedule (207)',
        'Alien Dictionary (269)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Dynamic Programming', [
        'Fibonacci Number (509)', 'Coin Change (322)', 'Climbing Stairs (70)',
        'House Robber (198)', 'House Robber II (213)', 'Palindromic Substrings (647)',
        'Longest Palindromic Substring (5)', 'Maximum Product Subarray (152)',
        'Decode Ways (91)', 'Word Break (139)', 'Longest Increasing Subsequence (300)',
        'Longest Common Subsequence (1143)', 'Unique Paths (62)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Greedy', [
        'Boats to Save People (881)', 'Maximum Subarray (53)', 'Jump Game (55)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Intervals', [
        'Merge Intervals (56)', 'Insert Interval (57)', 'Non-overlapping Intervals (435)',
        'Meeting Rooms (252)', 'Meeting Rooms II (253)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Matrix', [
        'Rotate Image (48)', 'Spiral Matrix (54)', 'Set Matrix Zeroes (73)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Bit Manipulation', [
        'Counting Bits (338)', 'Missing Number (268)', 'Number of 1 Bits (191)',
        'Reverse Bits (190)', 'Sum of Two Integers (371)',
    ]),
    ('21 · Master DSA / Blind 75+ (Sarda) — Bonus', [
        'Bonus',
    ]),
    # ===================== Computer architecture (Clements — replaces Sedgewick) =====================
    ('22 · Computer Architecture with Python & ARM (Clements) — Part 1: Simulating a Computer', [
        'Ch1: From Finite State Machines to Computers',
        'Ch2: High-Speed Introduction to Python', 'Ch3: Data Flow in a Computer',
        'Ch4: Crafting an Interpreter – First Steps', 'Ch5: A Little More Python',
        'Ch6: TC1 Assembler and Simulator Design', 'Ch7: Extending the TC1',
        'Ch8: Simulators for Other Architectures',
    ]),
    ('22 · Computer Architecture with Python & ARM (Clements) — Part 2: Raspberry Pi & ARM', [
        'Ch9: Raspberry Pi – An Introduction', 'Ch10: A Closer Look at the ARM',
        'Ch11: ARM Addressing Modes', 'Ch12: Subroutines and the Stack',
        'Appendices – Summary of Key Concepts',
    ]),
    # ===================== Frontend + interview strategy tail =====================
    ('23 · JavaScript Bootcamp (Freeman & Robson)', [
        'JavaScript Basics (variables, types, operators)',
        'Understanding Conditionals and Iteration', 'Understanding Functions',
        'Arrays & introducing the DOM', 'More Advanced DOM',
        'Event Handling and DOM Navigation',
    ]),
    ('24 · CSS Bootcamp (Lomidze) — Fundamentals', [
        'Introduction', 'Setup', 'What is CSS?', 'How to write CSS?',
        'HTML Elements Tree', 'CSS Selectors', 'CSS Combinators', 'CSS Colors',
        'Inheritance', 'Text Formatting - Part 1', 'Text Formatting - Part 2',
        'Box Model', 'Pseudo Classes - Part 1', 'Pseudo Classes - Part 2',
        'Pseudo Elements', 'Measurement Units - Part 1', 'Measurement Units - Part 2',
        'Positions - Part 1', 'Positions - Part 2', 'Overflow', 'Floats',
        'Practice Quiz — Fundamentals',
    ]),
    ('24 · CSS Bootcamp (Lomidze) — Backgrounds, Effects & Animations', [
        'Backgrounds - Part 1', 'Backgrounds - Part 2', 'Gradients', 'Shadows',
        'Transitions', 'Transforms - Part 1', 'Transforms - Part 2',
        'Animations - Part 1', 'Animations - Part 2', 'Practice Quiz — Effects',
    ]),
    ('24 · CSS Bootcamp (Lomidze) — Flexbox', [
        'What Is Flexbox?', 'Flex Container Properties', 'Flex Items Properties',
        'Practice Quiz — Flexbox',
    ]),
    ('24 · CSS Bootcamp (Lomidze) — Project: Grand Hotel', [
        'Grand Hotel - Project Preview', 'Sidebar - Markup', 'Sidebar - Style',
        'Navigation - Markup', 'Navigation - Style - Part 1',
        'Navigation - Style - Part 2', 'Create Click Event',
        'Create markup for Header', 'Header - Style', 'About Us Section - Markup',
        'About Us Section - Style - Part 1', 'About Us Section - Style - Part 2',
        'Rooms Section - Markup', 'Rooms Section - Style',
        'Customers Section - Markup', 'Customers Section - Style', 'Footer - Markup',
        'Footer - Style', 'Practice Quiz — Grand Hotel layout',
        'Make "Grand Hotel" Responsive - Part 1',
        'Make "Grand Hotel" Responsive - Part 2',
        'Make "Grand Hotel" Responsive - Part 3', 'Practice Quiz — Grand Hotel responsive',
    ]),
    ('24 · CSS Bootcamp (Lomidze) — CSS Grid', [
        'CSS Grid Introduction', 'Grid Setup', 'How to Create Grid',
        'Fractional Units', 'Positioning and Spanning Grid Items',
        'Naming Grid Items - Part 1', 'Naming Grid Items - Part 2',
        'Naming Grid areas', 'Explicit and Implicit Grid', 'Aligning Grid items',
        'Aligning Grid tracks', 'max-content, min-content, minmax()',
        'auto-fill, auto-fit', 'Practice Quiz — CSS Grid',
    ]),
    ('24 · CSS Bootcamp (Lomidze) — Project: Furniture Store', [
        'Furniture Store - Project Preview', 'Navbar - Part 1 - Markup',
        'Navbar - Part 1 - Style', 'Navbar - Search Form', 'Navbar - Part 2 - Markup',
        'Navbar - Part 2 - Style', 'Navbar - Part 2 - Dropdown', 'Banner - Markup',
        'Banner - Style', 'Banner Slideshow - Part 1', 'Banner Slideshow - Part 2',
        'Day Offer Section', 'Bestselling Furniture - Markup',
        'Bestselling Furniture - Style', 'Gallery', 'Contact Section and Footer',
        'Modal box - Markup', 'Modal Box - Style - Part 1', 'Modal Box - Style - Part 2',
        'Make Project Responsive', 'Practice Quiz — Furniture Store', 'Final Quiz',
    ]),
    ('25 · Network Engineer Interviewing Strategies (White)', [
        'The person (preparing, interviewer/interviewee perspectives, handling questions)',
        'Technical scope (detail questions, puzzle questions, aptitude questions)',
        'Team fit, following up & interview postmortems',
    ]),
    ('26 · Cracking the Frontend Coding Interview (Ahuja)', [
        'Applying for jobs (resume, cover letter, interview process)',
        'HTML & CSS skills (HTML5 tags, APIs, storage, Flexbox, Grid, positioning)',
        'JS coding round (scopes, closures, debounce/throttle, map/filter/reduce)',
        'Asynchronous JS (event loop, setTimeout, promises)',
        'Overcoming fears & problem-solving techniques',
    ]),
]

# Flatten into a single ordered list: [(section_name, item_name), ...]
ALL_ITEMS = [(sec, v) for sec, items in CURRICULUM for v in items]
TOTAL = len(ALL_ITEMS)

SAVE_PATH = Path(__file__).parent / "pivot_progress.json"


# ----------------------------------------------------------------------
# Persistence  (two states: completed + skipped)
# ----------------------------------------------------------------------
def load_progress() -> tuple[set[int], set[int]]:
    """Return (completed, skipped) sets of item indices (0-based)."""
    if not SAVE_PATH.exists():
        return set(), set()
    try:
        data = json.loads(SAVE_PATH.read_text())
        return set(data.get("completed", [])), set(data.get("skipped", []))
    except (json.JSONDecodeError, OSError):
        return set(), set()


def save_progress(completed: set[int], skipped: set[int]) -> None:
    """Persist completed + skipped indices to disk."""
    data = {"completed": sorted(completed),
            "skipped": sorted(skipped),
            "total": TOTAL}
    SAVE_PATH.write_text(json.dumps(data, indent=2))


# ----------------------------------------------------------------------
# App
# ----------------------------------------------------------------------
class TrackerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{APP_NAME} — Sep 2026 Study Tracker")
        self.root.geometry("980x680")
        self.root.minsize(740, 500)

        self.completed, self.skipped = load_progress()
        self.check_vars: list[tk.BooleanVar] = []
        # Per-item row widgets: (done_checkbutton, skip_button, base_label_text)
        self.row_widgets: list[tuple] = []
        # Per-section header refs: (label, base_name, start_idx, count)
        self.section_meta: list[tuple] = []
        self.target_date_var = tk.StringVar(value=TARGET_DEFAULT)

        self._build_ui()
        self._refresh_stats()

    def _build_ui(self):
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        left = ttk.Frame(container)
        left.pack(side="left", fill="both", expand=True)

        ttk.Separator(container, orient="vertical").pack(side="left", fill="y")

        side = ttk.Frame(container, padding=(14, 16, 16, 14))
        side.pack(side="right", fill="y")
        self._build_target_panel(side)

        header = ttk.Frame(left, padding=(16, 14, 16, 8))
        header.pack(fill="x")

        ttk.Label(header, text="Currently on",
                  font=("TkDefaultFont", 10)).pack(anchor="w")

        self.current_label = ttk.Label(header, text="",
                                       font=("TkDefaultFont", 14, "bold"))
        self.current_label.pack(anchor="w", pady=(2, 0))

        self.meta_label = ttk.Label(header, text="",
                                    font=("TkDefaultFont", 9),
                                    foreground="#666")
        self.meta_label.pack(anchor="w", pady=(2, 8))

        self.progress = ttk.Progressbar(header, length=440, mode="determinate",
                                        maximum=TOTAL)
        self.progress.pack(fill="x", pady=(4, 6))

        self.stats_label = ttk.Label(header, text="",
                                     font=("TkDefaultFont", 9))
        self.stats_label.pack(anchor="w")

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=4)

        body = ttk.Frame(left)
        body.pack(fill="both", expand=True, padx=8, pady=4)

        canvas = tk.Canvas(body, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical",
                                  command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=self.scroll_frame,
                                             anchor="nw")
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas_window, width=e.width)
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>",
                        lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>",
                        lambda e: canvas.yview_scroll(1, "units"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._populate_items()

        footer = ttk.Frame(left, padding=(16, 8, 16, 12))
        footer.pack(fill="x")
        ttk.Button(footer, text="Jump to current",
                   command=self._jump_to_current).pack(side="left")
        ttk.Button(footer, text="Reset all",
                   command=self._reset).pack(side="right")

    def _build_target_panel(self, parent):
        ttk.Label(parent, text="Target finish date",
                  font=("TkDefaultFont", 12, "bold")).pack(anchor="w")
        ttk.Label(parent, text="items/day needed to hit it",
                  font=("TkDefaultFont", 8), foreground="#888").pack(
                      anchor="w", pady=(0, 12))

        self.date_entry = ttk.Entry(parent, textvariable=self.target_date_var,
                                     width=14, justify="center")
        self.date_entry.pack(anchor="w")
        self.date_entry.bind("<Return>", lambda e: self._refresh_stats())
        self.date_entry.bind("<FocusOut>", lambda e: self._refresh_stats())

        ttk.Label(parent, text="format: YYYY-MM-DD",
                  font=("TkDefaultFont", 8), foreground="#aaa").pack(
                      anchor="w", pady=(2, 10))

        btn_row = ttk.Frame(parent)
        btn_row.pack(fill="x", anchor="w", pady=(0, 16))
        ttk.Button(btn_row, text="Sep 30", width=7,
                   command=lambda: self._set_target_date(TARGET_DEFAULT)).pack(
                       side="left", padx=(0, 4))
        for label, days in (("+1 mo", 30), ("+3 mo", 90)):
            ttk.Button(btn_row, text=label, width=6,
                       command=lambda d=days: self._set_target_days(d)).pack(
                           side="left", padx=(0, 4))

        self.rate_label = ttk.Label(parent, text="",
                                    font=("TkDefaultFont", 26, "bold"),
                                    foreground="#1a7f4b")
        self.rate_label.pack(anchor="w", pady=(4, 0))
        ttk.Label(parent, text="items / day",
                  font=("TkDefaultFont", 9), foreground="#666").pack(anchor="w")

        self.rate_sub_label = ttk.Label(parent, text="",
                                        font=("TkDefaultFont", 8),
                                        foreground="#888", wraplength=210,
                                        justify="left")
        self.rate_sub_label.pack(anchor="w", pady=(10, 0))

    def _set_target_days(self, days: int):
        from datetime import timedelta
        self.target_date_var.set((date.today() + timedelta(days=days)).isoformat())
        self._refresh_stats()

    def _set_target_date(self, iso: str):
        self.target_date_var.set(iso)
        self._refresh_stats()

    # ------------------------------------------------------------------
    # Item rows
    # ------------------------------------------------------------------
    def _populate_items(self):
        idx = 0
        for section_name, items in CURRICULUM:
            sec_frame = ttk.Frame(self.scroll_frame, padding=(8, 10, 8, 2))
            sec_frame.pack(fill="x")
            hdr = ttk.Label(sec_frame, text=section_name,
                            font=("TkDefaultFont", 11, "bold"))
            hdr.pack(side="left", anchor="w")
            start, count = idx, len(items)
            ttk.Button(sec_frame, text="skip section", width=12,
                       command=lambda s=start, n=count: self._skip_section(s, n)
                       ).pack(side="right")
            self.section_meta.append((hdr, section_name, start, count))

            for item in items:
                row = ttk.Frame(self.scroll_frame)
                row.pack(fill="x", padx=20, pady=1)
                base = f"  {idx + 1:>3}.  {item}"
                var = tk.BooleanVar(value=idx in self.completed)
                self.check_vars.append(var)
                cb = ttk.Checkbutton(row, text=base, variable=var,
                                     command=lambda i=idx: self._toggle(i))
                cb.pack(side="left", anchor="w")
                skip_btn = ttk.Button(row, text="skip", width=8,
                                      command=lambda i=idx: self._toggle_skip(i))
                skip_btn.pack(side="right")
                self.row_widgets.append((cb, skip_btn, base))
                idx += 1

        for i in range(TOTAL):
            self._apply_row_state(i)

    def _apply_row_state(self, idx: int):
        cb, skip_btn, base = self.row_widgets[idx]
        if idx in self.skipped:
            cb.state(["disabled"])
            cb.config(text=f"{base}    — skipped")
            skip_btn.config(text="undo")
        else:
            cb.state(["!disabled"])
            cb.config(text=base)
            skip_btn.config(text="skip")

    def _save(self):
        save_progress(self.completed, self.skipped)

    # ------------------------------------------------------------------
    # State toggles
    # ------------------------------------------------------------------
    def _toggle(self, item_idx: int):
        if self.check_vars[item_idx].get():
            self.completed.add(item_idx)
            self.skipped.discard(item_idx)
        else:
            self.completed.discard(item_idx)
        self._save()
        self._refresh_stats()

    def _toggle_skip(self, idx: int):
        if idx in self.skipped:
            self.skipped.discard(idx)
        else:
            self.skipped.add(idx)
            self.completed.discard(idx)
            self.check_vars[idx].set(False)
        self._apply_row_state(idx)
        self._save()
        self._refresh_stats()

    def _skip_section(self, start: int, n: int):
        rng = range(start, start + n)
        non_done = [i for i in rng if i not in self.completed]
        all_skipped = bool(non_done) and all(i in self.skipped for i in non_done)
        for i in non_done:
            if all_skipped:
                self.skipped.discard(i)
            else:
                self.skipped.add(i)
                self.check_vars[i].set(False)
            self._apply_row_state(i)
        self._save()
        self._refresh_stats()

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def _refresh_section_counts(self):
        for hdr, name, start, n in self.section_meta:
            done = sum(1 for i in range(start, start + n) if i in self.completed)
            sk = sum(1 for i in range(start, start + n) if i in self.skipped)
            cleared = done + sk
            mark = "  ✓" if cleared == n else ""
            extra = f", {sk} skipped" if sk else ""
            hdr.config(text=f"{name}   ·   {done}/{n}{extra}{mark}")

    def _refresh_stats(self):
        done = len(self.completed)
        skipped = len(self.skipped)
        cleared = done + skipped
        pct = (cleared / TOTAL) * 100
        self.progress["value"] = cleared

        next_idx = next((i for i in range(TOTAL)
                         if i not in self.completed and i not in self.skipped),
                        None)
        if next_idx is None:
            self.current_label.config(text="All cleared! 🎉")
            self.meta_label.config(text=f"{done} done · {skipped} skipped")
        else:
            section, item = ALL_ITEMS[next_idx]
            self.current_label.config(text=item)
            self.meta_label.config(
                text=f"{section} · Item {next_idx + 1} of {TOTAL}")

        remaining = TOTAL - cleared
        self.stats_label.config(
            text=(f"{done} done  ·  {skipped} skipped  ·  {remaining} left  ·  "
                  f"{pct:.1f}% cleared"))
        self._refresh_section_counts()
        self._refresh_target(remaining)

    def _refresh_target(self, remaining: int):
        if remaining <= 0:
            self.rate_label.config(text="Done! 🎉")
            self.rate_sub_label.config(text="Everything cleared (done or skipped).")
            return

        raw = self.target_date_var.get().strip()
        try:
            target = date.fromisoformat(raw)
        except ValueError:
            self.rate_label.config(text="—")
            self.rate_sub_label.config(text="Enter a valid date as YYYY-MM-DD.")
            return

        days = (target - date.today()).days
        if days <= 0:
            self.rate_label.config(text="—")
            self.rate_sub_label.config(
                text="Pick a date in the future to see a pace.")
            return

        per_day = remaining / days
        per_week = per_day * 7
        self.rate_label.config(text=f"{per_day:.1f}")
        self.rate_sub_label.config(
            text=(f"{remaining} items left in {days} days "
                  f"({target.strftime('%a, %b %d %Y')})\n"
                  f"≈ {per_week:.0f} items / week\n"
                  f"(skipping lowers this)")
        )

    def _jump_to_current(self):
        next_idx = next((i for i in range(TOTAL)
                         if i not in self.completed and i not in self.skipped),
                        None)
        if next_idx is None:
            messagebox.showinfo("Done", "Everything is cleared — nothing to jump to.")
            return
        self.scroll_frame.update_idletasks()
        canvas = self.scroll_frame.master
        canvas.yview_moveto(next_idx / TOTAL)

    def _reset(self):
        if not messagebox.askyesno(
            "Reset progress",
            "Clear all completed AND skipped items? This cannot be undone."
        ):
            return
        self.completed.clear()
        self.skipped.clear()
        for var in self.check_vars:
            var.set(False)
        for i in range(TOTAL):
            self._apply_row_state(i)
        self._save()
        self._refresh_stats()


def main():
    root = tk.Tk()
    TrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()