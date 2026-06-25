"""
Pivot — Sep 2026 Study Tracker
A tkinter desktop app tracking the full curated study curriculum
(Ultimate Flask Course + Linux + Protobuf + Network Automation +
Docker x2 + Microservices + book + DSA/CS + System Design + Blind 75).

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
# Sections are prefixed with the playlist item number (1-12).
# ----------------------------------------------------------------------
CURRICULUM = [
    # ===================== PHASE 1 — Flask core + Python craft foundations (use immediately) =====================
    ('1 · Flask — Ch1: Basics & Routing', [
        'Install Flask', 'Routing', 'Request Methods', 'Route Variables',
        'Query String Arguments', 'Form Data', 'JSON Data', 'Redirects', 'Debug Mode',
    ]),
    ('1 · Flask — Ch2: Templates (Jinja)', [
        'Intro to Templates', 'Template Variables', 'Conditionals', 'Loops', 'Include',
        'Inheritance', 'Comments', 'Static Files',
    ]),
    ('1 · Flask — Ch3: Database (SQLAlchemy)', [
        'Install and Configure', 'Create Table', 'Insert Data', 'Update Data',
        'Delete Data', 'Create One to Many Relationship',
        'Add Data to One to Many Relationship', 'Query One to Many Relationship',
        'Create Many to Many Relationship', 'Add Data to Many to Many Relationship',
        'Query Many to Many Relationship', 'Query All Data',
    ]),
    ('1 · Flask — Ch4: App Structure', [
        'App Factories', 'Organizing Projects Beyond a Single File', 'Blueprints',
    ]),
    ('13 · Pythonic OOP (Maxwell)', [
        'The Key Ideas of Powerful Objects', 'Writing Simple (and Useful) Python Classes',
        "Leveraging Methods (Python's special requirements)",
        'Encapsulation and Data Hiding', "Inheritance and 'is-a' Relationships",
        'The Different Kinds of Inheritance Hierarchies',
        'Interfaces and Abstract Methods',
        'The Single-Responsibility and Substitution Principles',
        'Gracefully Refactoring Your Classes as Requirements Evolve',
        'Python Data Classes', 'Wrap-up and Q&A',
    ]),
    ('18 · Pythonic Design Patterns (Maxwell)', [
        "Python's Object Syntax", 'Overview of Python Object Model Special Features',
        'Properties for Clean Design and Refactoring', 'Special Methods',
        'How OOP in Python Is Fundamentally Different from Other Languages',
        'The Observer Pattern', 'The Factory Patterns',
    ]),
    ('22 · Beyond Python Scripts — Exceptions, Error Handling & CLIs (Maxwell)', [
        "Python's Exception Model", 'Exception Patterns and Anti-patterns',
        'The Most Diabolical Python Anti-pattern (and How to Avoid It)',
        'Building Command-Line Programs', 'Bonus: Advanced Collection Types',
    ]),
    ('17 · Beyond Python Scripts — Logging, Modules & Dependencies (Maxwell)', [
        "Python's Logging System", 'Logging Design Patterns', 'Module Organization',
        'Evolving Reusable Python Modules as Requirements Change', 'Dependency Management',
    ]),
    # ===================== PHASE 2 — Your domain: protobuf, networking, concurrency (pli-mark / takproto / multicast) =====================
    ('3 · Protocol Buffers 3 (Maarek)', [
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
    ('4 · Python Sockets (Eramo) — Setup & Networking', [
        'Course Preview', 'Python Installation and Setup', 'VS Code Installation',
        'Creating our Working Directory', 'A Brief Overview of Networking Concepts',
    ]),
    ('4 · Python Sockets — TCP & UDP', [
        'Creating a TCP Server Socket', 'Creating a TCP Client Socket',
        'Sending Data through a TCP Connection',
        'Creating and Sending Data through a UDP Server/Client',
        'Exploring the Buffer Size',
    ]),
    ('4 · Python Sockets — Threading Basics', [
        'The Threading Module Basics Pt 1', 'The Threading Module Basics Pt 2',
    ]),
    ('4 · Python Sockets — Serialization (Pickle/JSON)', [
        'The Pickle Module — Sending Objects through the Data Stream',
        'The JSON Module — Sending Objects through the Data Stream',
    ]),
    ('4 · Python Sockets — Fixed-Length Headers', [
        'Fixed-Length Headers — Shortcomings of a Fixed Max Byte Size',
        'Fixed-Length Headers — The Solution',
    ]),
    ('14 · Scaling Python with Generators (Maxwell)', [
        'Pythonic Scalability Overview',
        'Generators for Efficient, Scalable, Well-Encapsulated Code',
        "Demystifying Python's Iterator Protocol",
        'Understanding Views, Iterators, and Iterables',
        'Patterns for Scalable Composability',
        'Rich and Expressive Data Structures Overview', 'List Comprehensions',
        'Comprehensions of Dicts, Sets, and More', 'Generator Comprehensions',
    ]),
    ('15 · Concurrency in Python (Prasad)', [

        'Python Thread Overview (GIL, kernel threads, CPython internals, nonblocking I/O, C extensions)',
        'Locks and Semaphores', 'Queues — Share Memory by Communicating',
        'Multiprocessing — Concurrency and Parallelism',
        'Coroutines — Concurrency from Scratch', 'Gevent — Greenlets and Monkey Patching',
        'AsyncIO — async/await, Event Loops, Concurrent Futures',
        'Hacks — A Grab-bag of Async Ideas',
    ]),
    ('23 · Threading in Python (Gaines)', [
        'What Is a Thread?', 'Build a Single-Threaded Application',
        'Build a Simple Multithreaded Application', 'Daemon Threads',
        'Convert a Multithreaded App to Use Daemon Threads', 'Joining Threads (.join())',
        'Create, Start, and Join Multiple Threads Using a Loop', 'ThreadPoolExecutor',
        'Race Conditions', 'Thread Synchronization Using Locks (deadlock)',
        'Wrap-up and Q&A',
    ]),
    # ===================== PHASE 3 — Flask depth for real services (APIs, data, auth, realtime) =====================
    ('1 · Flask — SQLAlchemy Fundamentals', [
        'Setting Up A Database and Determining the URI', 'Installing Flask-SQLAlchemy',
        'Connecting to the Database', 'Create a Table', 'Inserting Data', 'Updating Data',
        'Deleting Data',
    ]),
    ('1 · Flask — SQLAlchemy Query Deep Dive', [
        'Intro to Queries', 'Generative Queries', 'Not Equals and Like', 'In and Not In',
        'Null and Not Null', 'And', 'Or', 'Order By', 'Limit', 'Offset', 'Count',
        'Inequality', 'One to Many Relationships', 'One to Many Queries',
        'Many to Many Relationships', 'Many to Many Queries',
    ]),
    ('1 · Flask — SQLAlchemy Relationships & Reporting', [
        'Install and Set Up', 'Create the Models', 'Create the Relationships',
        'Create the Database', 'Insert Data', 'Updating Data', 'Deleting Data',
        'Populating the Database', 'Get All Customer Orders', 'Get All Pending Orders',
        'How Many Customers', 'Get Orders With Coupon Codes', 'Get Revenue in Past X Days',
        'Get the Average Fulfillment Time',
        'Get Customers Who Have Purchased More Than $X',
    ]),
    ('1 · Flask — Ch6: REST API (intro)', [
        'Postman', 'Organize Files', 'Add JSON to Method', 'Get Members Route',
        'Get One Member', 'Create a Member', 'Edit a Member',
    ]),
    ('1 · Flask — Flask-WTF (WTForms)', [
        'Install and Set Up', 'Creating a Form', 'Submit the Form', 'Validators',
        'More Fields', 'Adding An Extra Validator', 'Changing Labels and Defaults',
        'Prepopulating Data', 'Populate Obj', 'More on CSRF', 'Jinja Macro',
        'Form Inheritance', 'Field Enclosures', 'Field List', 'Delete Field',
        'Dynamic Forms', 'Note on JavaScript AJAX', 'Recaptcha Field', 'Inline Validators',
        'Information on Other Fields and Validators', 'Date Fields', 'Flask-WTF Example',
        'Flask-WTF with Flask-Bootstrap',
    ]),
    ('1 · Flask — Flask-Migrate', [
        'Installation and Environment Variable Setup',
        'Creating Database, Adding SQLAlchemy and Migrate',
        'Create Table Upgrade in SQLite', 'Upgrading With SQLite', 'SQLite Downgrades',
        'Upgrading and Downgrading', 'MySQL Upgrade and Downgrade',
        'Manually Edit Migration', 'Dropping Columns in SQLite',
    ]),
    ('1 · Flask — Flask-Login (deep)', [
        'Installation and Init', 'Add User Model', 'The User Loader', 'Login User',
        'Current User', 'Logout User', 'Creating a Login Form', 'Redirect to Login Route',
        'Login Message', 'Redirect', 'Remember Me', 'Fresh Login', 'Auto Expire',
        'Alternative Tokens', 'Using MongoDB',
    ]),
    ('1 · Flask — Flask-Security', [
        'Installation and Setup', 'Create Database', 'View Login and Register Routes',
        'Additional Routes', 'Login Required and Current User', 'Roles', 'Enabling Emails',
        'Custom Emails', 'Custom Views', 'Extending the Forms', 'HTTP Basic Auth',
    ]),
    ('1 · Flask — Flask-Restless', [
        'Installation', 'Setup Models', 'Create Database', 'Integrate Flask-Restless',
        'GET Requests', 'GET Specific Items', 'POST Requests', 'DELETE Requests',
        'PUT Requests', 'Limit', 'Offset', 'Order By', 'Search Queries',
        'In and Not in Operators', 'Is Null and Is Not Null Operators', 'Like Operator',
        'Or Queries', 'Any Operator', 'Has Operator', 'Deleting With Queries',
        'Patch With Queries Bug', 'Pagination',
    ]),
    ('1 · Flask — Flask-SocketIO', [
        'Installation and Setup', 'Setting Up JavaScript Client',
        'Sending From Client to Server', 'Sending From Server to Client',
        'Emit Custom Events', 'Sending and Receiving JSON', 'Multiple Clients',
        'Broadcasting Messages', 'Server Initiated Events', 'Namespaces', 'Session IDs',
        'Send Private Message', 'Join Room', 'Leave Room', 'Close Room',
        'Connect and Disconnect',
    ]),
    ('1 · Flask — Flask-Mail', [
        'Configuration', 'Set Up Server and Send Email', 'Note on Debug', 'Email Body',
        'Adding More Recipients', 'Adding Sender Name', 'Bulk Messages', 'Attachments',
        'Other Message Parameters', 'Setting Up Gmail',
    ]),
    ('1 · Flask — Ch5: Form & Data Project', [
        'Setup Project and Display Template', 'Setting Up The Models', 'Setup Database',
        'Seed Topic and Language Data', 'Setup Password Hash',
        'Verify Form Data is Being Submitted', 'Load Languages and Topics',
        'Save Data From Form', 'Load Existing Data', 'Update Database With New Data',
        'Error Handling',
    ]),
    ('1 · Flask — Ch7: Dashboard Project', [
        'Overview of Templates', 'Setup Flask App and Templates',
        'Create Models for Dashboard', 'Command to Create Tables',
        'Add Data Into Database', 'Overview of Queries We Need',
        'Writing the Queries Part One', 'Writing the Queries Part Two',
        'Writing the Queries Part Three', 'Writing the Queries Part Four',
        'Add the Card Values', 'Add the Revenue Goals', 'Work With Area Chart',
        'Work With Pie Chart', 'Work With Bar Chart', 'Fill in Order Table',
        'Setup Flask Login', 'Protecting the Routes', 'Register a User', 'Log In User',
        'Add Password Hashing', 'Log Out User', 'Update Link', 'Add Current User Name',
        'Add Remember Me', 'Format Numbers and Dates', 'Fix Pie Chart Numbers',
        'Form Validation',
    ]),
    # ===================== PHASE 4 — Python mastery, deployment, pivot/interview prep =====================
    ('21 · Python: The Next Level (Maxwell)', [
        'Variable-Argument Functions', 'Leveraging Argument Unpacking',
        'Understanding Function Objects in Python', 'Using Key Functions',
        'Writing Code That Takes Functions as Arguments',
        'The Amazing Benefits of Decorators', 'Basic Structure of the Decorator',
        'Common Decorator Patterns and Best Practices',
        'Quick Review of Key Decorator Patterns', 'Decorators Taking Arguments',
        'Class-Based Decorators', 'Magic Methods for Custom Syntax and Natural Semantics',
        'Custom Container Classes', 'Iterable Sequence Containers', 'Index and Key Access',
    ]),
    ('16 · Test-Driven Development in Python (Maxwell)', [
        'Why Writing Tests Is a Superpower', 'The Different Kinds of Automated Tests',
        'Testing Frameworks: The unittest Module', 'Unit Tests and Simple Assertions',
        'Lab: The Text Body', 'Test Organization', 'Fixtures and Common Test Setup',
        'Asserting Exceptions', 'Subtests for Parameterized Tests',
        'Lab: More Advanced Testing', 'Mocks for Rapid Indirect Testing',
        'Tooling for Test Automation', 'The Popular Pytest Framework',
    ]),
    ('20 · Python for Applications: Beyond Scripts (Maxwell)', [
        "Python's Logging System", 'Logging Design Patterns', "Python's Exception Model",
        'Exception Patterns & Anti-patterns', 'Module Organization',
        'Evolving Reusable Python Modules as Requirements Change',
        'Automated Tests and Unit Tests', 'Test-Driven Development',
        'Building Command-Line Programs',
    ]),
    ('19 · Python: Beyond the Basics (Maxwell)', [
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
    ('2 · Linux Fundamentals (van Vugt)', [
        'Linux Distributions & Installation', 'Connecting to Linux (root, su/sudo, SSH)',
        'Essential Tools (command line, man)', 'Files & Directories',
        'Working with Text Files (vi, regex)',
        'The Bash Shell (redirection, piping, history)', 'Users & Basic Permissions',
        'Storage Management (mount)', 'Managing Processes', 'Managing Software',
    ]),
    ('5 · Docker Fundamentals (Kane)', [
        'Introduction (Docker terminology)', 'Building Images (Dockerfile, Docker Hub)',
        'Advanced Building I (small images, multistage, debug)',
        'Advanced Building II (layering, ordering, private registry)',
        'Containers Intro (history, why Docker)',
        'Container Details (ports, volumes, logs, stats, events)',
        'Debugging & Resources (kernel, debug, resource control)',
        'Container Security (UID, privileged, capabilities, seccomp)',
    ]),
    ('6 · Docker Microservices Workshop (Kocherhin)', [
        'Introduction', 'Why Do You Need Docker?', 'Planning Docker Application',
        'Installing Docker Tools', 'Creating Dockerfile', 'Creating API Application',
        'Preparing API Docker Image', 'Starting API Server', 'Docker Hub',
        'Environment Variables', 'Adding Database', 'Making Database Requests', 'Volumes',
        'Auth Service', 'Frontend Service', 'Running Frontend in Production',
        'Docker Exec', 'Setting Up Nginx', 'Proxying API Requests', 'Docker Network',
        'Frontend Proxy', 'Last Tuning', 'Do It Yourself: Mailer Service',
    ]),
    ('7 · Microservices Bootcamp (Newman)', [
        'What Microservices Are', 'The Problem with Coupling', 'Domain-Driven Design',
        'Boundaries, Teamwork & Communication Patterns',
        'Deployment, Troubleshooting, Observability',
    ]),
    ('8 · Docker Microservices w/ Python — Book (Buelta)', [
        'Making the Move - Design, Plan, Execute', 'Creating a REST Service with Python',
        'Build, Run, Test Your Service Using Docker', 'Creating a Pipeline and Workflow',
        'Using Kubernetes to Coordinate Microservices',
        'Local Development with Kubernetes',
        'Configuring and Securing the Production System', 'Using GitOps Principles',
        'Managing Workflows', 'Monitoring Logs and Metrics',
        'Handling Change, Dependencies, and Secrets', 'Collaborating Across Teams',
    ]),
    ('9 · Algorithms & Data Structures (Heineman)', [
        'log(n) behavior / Binary Array Search',
        'Basic Data Structures (queue, stack, deque, bag, symbol table, heap, graph)',
        'Sorting (TimSort, InsertionSort, MergeSort)', 'Graph Algorithms',
        'Skip List Implementation',
    ]),
    ('10 · Computer Science — Part II (Sedgewick)', [
        'Intro to Part II', 'Lec 11: Searching and Sorting', 'Lec 12: Stacks and Queues',
        'Lec 13: Symbol Tables', 'Lec 14: Theory of Computation',
        'Lec 15: Turing Machines', 'Lec 16: Intractability (P/NP)',
        'Lec 17: A Computing Machine', 'Lec 18: von Neumann Machines',
        'Lec 19: Combinational Circuits', 'Lec 20: CPU',
    ]),
    ('11 · System Design Interview (Bhardwaj)', [
        'System Design Basics', 'Architecture Basics',
        'Mock: Taxi / Streaming / Real-Time Analytics',
        'Mock: News Feed / URL Shortener / Auction', 'Mock: Shopping / Booking / Coupon',
        'Mock: Chat / Taxi / Recommendations', 'Mock: Fraud / Sentiment / Product Search',
        'Challenges, Questions & Tips',
    ]),
    ('12 · Blind 75 — Start Here', [
        'Course Introduction', 'Resources / Speed / Recommendations',
    ]),
    ('12 · Blind 75 — Arrays & Hashing', [
        'Two Sum (1)', 'Contains Duplicate (217)', 'Valid Anagram (242)',
        'Group Anagrams (49)', 'Top K Frequent Elements (347)', 'Is Subsequence (392)',
        'Longest Consecutive Sequence (128)', 'Product of Array Except Self (238)',
    ]),
    ('12 · Blind 75 — Two Pointers', [
        'Valid Palindrome (125)', 'Two Sum II (167)', '3Sum (15)',
        'Container With Most Water (11)',
    ]),
    ('12 · Blind 75 — Sliding Window', [
        'Maximum Average Subarray I (643)', 'Best Time to Buy and Sell Stock (121)',
        'Longest Repeating Character Replacement (424)',
        'Longest Substring Without Repeating Characters (3)',
        'Minimum Window Substring (76)',
    ]),
    ('12 · Blind 75 — Linked List', [
        'Middle of the Linked List (876)', 'Linked List Cycle (141)',
        'Linked List Cycle II (142)', 'Reverse Linked List (206)', 'Reorder List (143)',
        'Remove Nth Node From End of List (19)', 'Merge Two Sorted Lists (21)',
        'Merge k Sorted Lists (23)',
    ]),
    ('12 · Blind 75 — Stack', [
        'Valid Parentheses (20)', 'Daily Temperatures (739)',
    ]),
    ('12 · Blind 75 — Binary Search', [
        'Binary Search (704)', 'Find Minimum in Rotated Sorted Array (153)',
        'Search in Rotated Sorted Array (33)',
    ]),
    ('12 · Blind 75 — Trees (DFS/BFS)', [
        'Invert Binary Tree (226)', 'Maximum Depth of Binary Tree (104)',
        'Same Tree (100)', 'Subtree of Another Tree (572)',
        'Lowest Common Ancestor of a BST (235)', 'Binary Tree Level Order Traversal (102)',
        'Validate Binary Search Tree (98)', 'Kth Smallest Element in a BST (230)',
        'Construct Binary Tree from Preorder and Inorder (105)',
        'Binary Tree Maximum Path Sum (124)',
        'Serialize and Deserialize Binary Tree (297)',
    ]),
    ('12 · Blind 75 — Backtracking', [
        'Combination Sum (39)', 'Word Search (79)',
    ]),
    ('12 · Blind 75 — Tries', [
        'Implement Trie (208)', 'Add and Search Words Data Structure (211)',
        'Word Search II (212)',
    ]),
    ('12 · Blind 75 — Heap / Priority Queue', [
        'Find Median from Data Stream (295)',
    ]),
    ('12 · Blind 75 — Graphs', [
        'Number of Islands (200)', 'Clone Graph (133)',
        'Pacific Atlantic Water Flow (417)', 'Graph Valid Tree (261)',
        'Number of Connected Components (323)', 'Course Schedule (207)',
        'Alien Dictionary (269)',
    ]),
    ('12 · Blind 75 — Dynamic Programming', [
        'Fibonacci Number (509)', 'Coin Change (322)', 'Climbing Stairs (70)',
        'House Robber (198)', 'House Robber II (213)', 'Palindromic Substrings (647)',
        'Longest Palindromic Substring (5)', 'Maximum Product Subarray (152)',
        'Decode Ways (91)', 'Word Break (139)', 'Longest Increasing Subsequence (300)',
        'Longest Common Subsequence (1143)', 'Unique Paths (62)',
    ]),
    ('12 · Blind 75 — Greedy', [
        'Boats to Save People (881)', 'Maximum Subarray (53)', 'Jump Game (55)',
    ]),
    ('12 · Blind 75 — Intervals', [
        'Merge Intervals (56)', 'Insert Interval (57)', 'Non-overlapping Intervals (435)',
        'Meeting Rooms (252)', 'Meeting Rooms II (253)',
    ]),
    ('12 · Blind 75 — Matrix', [
        'Rotate Image (48)', 'Spiral Matrix (54)', 'Set Matrix Zeroes (73)',
    ]),
    ('12 · Blind 75 — Bit Manipulation', [
        'Counting Bits (338)', 'Missing Number (268)', 'Number of 1 Bits (191)',
        'Reverse Bits (190)', 'Sum of Two Integers (371)',
    ]),
    ('12 · Blind 75 — Bonus', [
        'Bonus',
    ]),
    # ===================== PHASE 5 — Deferrable tail (niche extensions, generic project clones, sockets filler) =====================
    ('1 · Flask — Flask-Bootstrap', [
        'Installation Setup', 'Blank HTML', 'Available Blocks',
    ]),
    ('1 · Flask — Flask-Uploads', [
        'Installation and Configuration', 'Upload Form', 'Uploading First Image',
        'Allow and Deny', 'Default Dest', 'Combining Extensions',
    ]),
    ('1 · Flask — Flask-Admin', [
        'Install and Setup', 'Add User View', 'View of Table With Multiple Columns',
        'Table with Relationship', 'Remove Column from View', 'Display Primary Key Column',
        'Enable/Disable Create, Edit, and Delete', 'Export Table Data', 'Create Modal',
        'Other Attributes', 'Using on_model_change to Automatically Hash Password',
        'File Admin', 'Modifying the Home Template', 'Modifying Other Views',
        'Creating a New View', 'URL For', 'Inline Models', 'Auth for Views',
        'Adding Flask-Login',
    ]),
    ('1 · Flask — Flask-User', [
        'Installation and Configuration', 'Create Database',
        'Flask-User Sign In and Register Screens', 'Create Protected Page',
        'What Flask-User Does to Database Record', 'Enabling Emails',
        'Modifying Templates', 'Modifying Email Templates',
        'Changing the After Register Endpoint', 'Current User Information',
    ]),
    ('1 · Flask — Flask-Babel (i18n)', [
        'Install Flask-Babel', 'Locale', 'Dates and Datetime',
        'Marking Words for Translation', 'Translations', 'Poedit',
    ]),
    ('1 · Flask — Project: Food/Calorie Tracker (→ Lightsail)', [
        'Demo', 'The Starting HTML Files', 'Adding Templates', 'Creating the Database',
        'Adding Database Helpers', 'Working With The Food Form',
        'Inserting Food Data Into Database', 'Display All Foods in Database',
        'Inserting the Date', 'Query All Dates', 'Day Screen', 'Add Food to Database',
        'Get List Of Foods For Day', 'Getting Food Totals For Day', 'Links',
        'Sum Totals Per Day', 'Adding Links', 'Refactor',
        'Deployment Server Setup on Amazon Lightsail', 'Deploy To Amazon Lightsail Server',
        'Errata',
    ]),
    ('1 · Flask — Project: Q&A App (→ Heroku/Postgres)', [
        'Demo', 'Overview of Templates', 'Install and Templates', 'Database Helpers',
        'Creating the Database', 'Register User', 'Login', 'Sessions',
        'Common User Function', 'Updating Links', 'Creating Test Users', 'User Setup Page',
        'Create Question', 'List Questions', 'Answer Question', 'Home Route Questions',
        'Question Page', 'Preventing Duplicate Users', 'Protecting Routes',
        'Protecting Routes by Role', 'Login Failure Messages', 'Formatting Queries',
        'Added Link Macro', 'Base Template', 'Deploy to Heroku', 'Convert to Postgres',
        'Static Secret Key On Heroku',
    ]),
    ('1 · Flask — Project: REST API (→ PythonAnywhere)', [
        'Demo', 'Setting Up The App and Test With Postman', 'Adding Database Helpers',
        'Create the Database', 'Create a New Member', 'Return Member After Creation',
        'Get All Members', 'Get One Member', 'Edit A Member', 'Delete A Member',
        'Authentication', 'Authentication Decorator', 'Deploy to Python Anywhere',
    ]),
    ('1 · Flask — Project: Twitter Clone', [
        'Overview of Templates', 'Create Routes With Templates',
        'Convert Static Resources', 'Prepare Flask-Migrate and Flask-SQLAlchemy',
        'Create SQLite Database', 'Add User Model and Create Table',
        'Creating the Register Form', 'Convert Register Form to WTForm',
        'Testing the Register Form', 'Adding Error Messages to Register Form',
        'Handling the Profile Image Upload', 'Save Registration Data to Database',
        'Creating the Login Form', 'Creating the Login Route', 'Finishing the Login Form',
        'Displaying the Profile Information', 'Create Tweet Model and Migrate',
        'Create Tweet Form', 'Update Timeline to Be Dynamic',
        'Add Time Since Tweet Created', 'First Refactor',
        'Timeline Image and Total Tweets', 'General Timeline Page', 'Make Profile General',
        'Follower Model', 'Add Follow Route',
        'Update Follower Count and List of Followers', 'Create Follow Link',
        'Test Follow Link', 'Update Timeline Page', 'Add Links to User Profiles',
        'Who to Watch Section', 'Add User Timeline Links', 'Refactor HTML',
        'Refactor Navigation', 'Make Navigation Links Dependent on Login Status',
        'Update Timeline Follower Count and Change Homepage', 'Refactor Views',
        'Refactor Register Template', 'Conclusion',
    ]),
    ('1 · Flask — Project: E-commerce Store', [
        'Starting Files', 'Adding the Product Table', 'Creating the Add Product Form',
        'Add Products to Database', 'Admin Dashboard Product List',
        'Showing the Dollar Amount and Product Counts', 'Adding Products to Homepage',
        'The Product Page', 'Adding to the Cart', 'The Cart Session',
        'Display the Items in Cart', 'Remove Item From Cart', 'Creating the Order Tables',
        'Creating the Checkout Form', 'Checkout Form Continued', 'Checkout Form Finalized',
        'Randomizing the Reference', 'Checkout Screen Cart Details',
        'Admin Pending Orders', 'Calculating the Order Total', 'Order Screen',
        'Updating the Stock Totals',
    ]),
    ('1 · Flask — Project: Forum', [
        'Overview of App', 'Setting up the Flask-Security Models',
        'Setting Up the Register Page', 'Setting Up A User', 'Login Screen',
        'Thread Model', 'Saving the Thread Form to Database',
        'Displaying Threads from the Database',
        'Updating the Thread Model to Include Date', 'Thread Page',
        'Creating the Reply Model', 'Handling Replies', 'Last Post Date',
        'The Profile Page', 'Adding Links and Wrap Up',
    ]),
    ('1 · Flask — Project: Weather App', [
        'Intro', 'Set Up App', 'Retrieve API Data', 'Create Database',
        'Add Cities to Database', 'Show Saved City Data', 'Allow User Save Cities',
        'Install Python-Dotenv', 'Prevent Duplicate Cities', 'Prevent Invalid Cities',
        'Message Flashing', 'Deleting Cities',
    ]),
    ('4 · Python Sockets — Basic Two-Way Chat', [
        'Basic Two-Way Chat Pt 1 — Server/Client Setup',
        'Basic Two-Way Chat Pt 2 — Enabling the Chat',
    ]),
    ('4 · Python Sockets — Terminal Chat Room', [
        'Terminal Chat Room Pt 1 — Server/Client Setup',
        'Terminal Chat Room Pt 2 — Adding Functionality',
        'Terminal Chat Room Pt 3 — Adding Functionality',
        'Terminal Chat Room Pt 4 — Functionality & Testing',
    ]),
    ('4 · Python Sockets — Tkinter Module', [
        'Tkinter — Defining a Root Window', 'Tkinter — Adding Frames',
        'Tkinter — Adding Widgets', 'Tkinter — Adding Functionality',
    ]),
    ('4 · Python Sockets — Basic GUI Chat Room', [
        'Basic GUI Chat Pt 1 — Client Layout', 'Basic GUI Chat Pt 2 — Client Layout',
        'Basic GUI Chat Pt 3 — Adding Functionality',
        'Basic GUI Chat Pt 4 — Functionality & Testing',
    ]),
    ('4 · Python Sockets — Advanced GUI Chat Room', [
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
    ('4 · Python Sockets — WAN / Network Config', [
        'Adjusting Host Firewall for LAN Communication',
        'Setting a Static IP Address for WAN Communication',
        'Enabling Port Forwarding for WAN Communication', 'Testing out WAN Communication',
        'Configuring a Second Router (Different Settings)',
    ]),
    ('4 · Python Sockets — Pygame Module', [
        'Pygame — Creating a Game Window and Game Loop',
        'Pygame — Setting Up a Game Class', 'Pygame — Setting Up a Player Class',
    ]),
    ('4 · Python Sockets — Online Multiplayer Game', [
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