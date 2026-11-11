from .extensions import db
from .models import Question, Resource, Topic

CONTENT = [
    {
        "name": "Python Programming",
        "icon": "🐍",
        "description": "Core Python syntax, data types, functions, comprehensions and the runtime.",
        "questions": [
            (1, "What is the output of print(type([]))?", ["<class 'list'>", "<class 'tuple'>", "<class 'dict'>", "<class 'set'>"], "An empty square-bracket literal creates a list object."),
            (1, "Which keyword is used to define a function in Python?", ["def", "func", "function", "define"], "Functions are declared with the def keyword."),
            (1, "Which of these built-in types is immutable?", ["tuple", "list", "dict", "set"], "Tuples cannot be modified after creation; lists, dicts and sets can."),
            (2, "What does len({1, 2, 2, 3}) return?", ["3", "4", "2", "1"], "A set stores unique values only, so the duplicate 2 is dropped."),
            (2, "What does [x * x for x in range(4)] produce?", ["[0, 1, 4, 9]", "[1, 4, 9, 16]", "[0, 1, 2, 3]", "[0, 2, 4, 6]"], "range(4) yields 0 to 3 and each value is squared."),
            (2, "What does *args do in a function definition?", ["Collects extra positional arguments into a tuple", "Collects keyword arguments into a dictionary", "Makes every argument mandatory", "Unpacks only dictionaries"], "*args gathers surplus positional arguments as a tuple; **kwargs handles keywords."),
            (3, "Which keyword turns a function into a lazy generator?", ["yield", "return", "break", "pass"], "yield suspends the function and produces values one at a time."),
            (3, "What is the output of print(bool([]), bool('0'))?", ["False True", "False False", "True True", "True False"], "An empty list is falsy, but the non-empty string '0' is truthy."),
            (3, "What does the GIL in CPython do?", ["Lets only one thread execute Python bytecode at a time", "Compiles Python to machine code", "Manages memory garbage collection only", "Prevents any use of threads"], "The Global Interpreter Lock serialises bytecode execution across threads."),
        ],
        "resources": [
            ("Official Python Tutorial", "https://docs.python.org/3/tutorial/", "Documentation", 1, "Official walkthrough of python basics: data types, list, tuple, set, dict, functions and the def keyword.", "python basics types list tuple immutable def function"),
            ("W3Schools Python Tutorial", "https://www.w3schools.com/python/", "Tutorial", 1, "Interactive python examples covering syntax, type checks, loops, functions and collections.", "python syntax type loops functions collections"),
            ("Real Python Learning Paths", "https://realpython.com/", "Articles", 2, "Deep dives on list comprehension, set length, *args and **kwargs, iterators and generator expressions.", "comprehension args kwargs set len iterator generator"),
            ("Understanding the Python GIL", "https://realpython.com/python-gil/", "Article", 3, "Global interpreter lock, threads, yield based lazy generators, truthiness of bool values and decorators.", "gil threads yield generator bool truthiness decorator"),
        ],
    },
    {
        "name": "Data Structures",
        "icon": "🌳",
        "description": "Arrays, stacks, queues, trees, graphs, hashing and algorithm complexity.",
        "questions": [
            (1, "Which data structure follows the LIFO principle?", ["Stack", "Queue", "Array", "Linked list"], "A stack removes the most recently pushed element first."),
            (1, "What is the time complexity of reading an array element by index?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "Index access computes the memory address directly."),
            (1, "Which data structure follows the FIFO principle?", ["Queue", "Stack", "Tree", "Graph"], "A queue serves elements in the order they arrived."),
            (2, "What is the worst-case time complexity of binary search?", ["O(log n)", "O(n)", "O(n log n)", "O(1)"], "Each step halves the remaining search space."),
            (2, "Which traversal of a binary search tree visits keys in sorted order?", ["Inorder", "Preorder", "Postorder", "Level order"], "Inorder visits left subtree, node, then right subtree."),
            (2, "Which data structure is typically used to implement breadth-first search?", ["Queue", "Stack", "Heap", "Hash table"], "BFS explores level by level, which needs FIFO ordering."),
            (3, "What is the average-case insertion time in a hash table with a good hash function?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "Well distributed keys give constant time operations on average."),
            (3, "Which sorting algorithm guarantees O(n log n) in the worst case?", ["Merge sort", "Quick sort", "Bubble sort", "Insertion sort"], "Merge sort always splits evenly; quick sort can degrade to O(n^2)."),
            (3, "What is the minimum number of edges in a connected undirected graph with n vertices?", ["n - 1", "n", "n + 1", "n(n - 1)/2"], "A spanning tree connects n vertices using exactly n - 1 edges."),
        ],
        "resources": [
            ("Data Structures Basics", "https://www.geeksforgeeks.org/data-structures/", "Tutorial", 1, "Introduction to arrays, stack LIFO, queue FIFO, linked list and index access in O(1).", "array stack queue lifo fifo linked list index"),
            ("Big-O Notation Explained", "https://www.geeksforgeeks.org/analysis-of-algorithms-big-o-analysis/", "Tutorial", 1, "Understand time complexity, O(1), O(n), O(log n) and how to compare algorithms.", "big o time complexity analysis algorithms"),
            ("Binary Search Trees and Traversals", "https://www.geeksforgeeks.org/binary-search-tree-data-structure/", "Tutorial", 2, "Binary search tree, inorder traversal giving sorted order, binary search in log n, BFS with a queue.", "binary search tree inorder traversal bfs queue"),
            ("Hashing Data Structure", "https://www.geeksforgeeks.org/hashing-data-structure/", "Tutorial", 3, "Hash table collisions and average O(1) insertion, merge sort n log n, graph edges and spanning trees.", "hash table collision merge sort graph spanning tree edges"),
        ],
    },
    {
        "name": "Database Management",
        "icon": "🗄️",
        "description": "SQL queries, joins, transactions, normalization and indexing.",
        "questions": [
            (1, "Which SQL command retrieves data from a table?", ["SELECT", "INSERT", "UPDATE", "DELETE"], "SELECT reads rows; the others modify data."),
            (1, "What does a primary key do?", ["Uniquely identifies each row", "Allows duplicate rows", "Stores binary images", "Encrypts the table"], "A primary key is unique and non-null for every row."),
            (1, "Which SQL clause filters rows before grouping?", ["WHERE", "ORDER BY", "GROUP BY", "LIMIT"], "WHERE restricts rows; HAVING restricts groups."),
            (2, "Which join returns all rows from the left table plus matches from the right?", ["LEFT JOIN", "INNER JOIN", "CROSS JOIN", "NATURAL JOIN"], "LEFT JOIN keeps unmatched left rows with NULLs on the right."),
            (2, "In ACID, what does the letter I stand for?", ["Isolation", "Integrity", "Indexing", "Inheritance"], "Isolation keeps concurrent transactions from interfering."),
            (2, "Which clause filters groups after GROUP BY?", ["HAVING", "WHERE", "FILTER", "LIMIT"], "HAVING is evaluated after aggregation."),
            (3, "A table is in 3NF if it is in 2NF and has no what?", ["Transitive dependencies", "Partial dependencies", "Multivalued attributes", "Composite keys"], "3NF removes non-key attributes depending on other non-key attributes."),
            (3, "Which index structure do most relational databases use?", ["B+ tree", "Linked list", "Stack", "Trie"], "B+ trees keep keys sorted and support fast range scans."),
            (3, "Which problem occurs when a transaction reads data another transaction has not committed?", ["Dirty read", "Phantom read", "Lost commit", "Deadlock"], "A dirty read sees uncommitted changes that may roll back."),
        ],
        "resources": [
            ("SQL Tutorial", "https://www.w3schools.com/sql/", "Tutorial", 1, "Learn select, insert, update, delete, where clause and primary key with live examples.", "sql select where primary key insert update delete"),
            ("SQL Joins Explained", "https://www.w3schools.com/sql/sql_join.asp", "Tutorial", 2, "Left join, inner join, group by and having clause with aggregate functions.", "left join inner join group by having aggregate"),
            ("ACID Properties in DBMS", "https://www.geeksforgeeks.org/acid-properties-in-dbms/", "Tutorial", 2, "Atomicity, consistency, isolation and durability of database transactions.", "acid atomicity consistency isolation durability transaction"),
            ("Normal Forms in DBMS", "https://www.geeksforgeeks.org/normal-forms-in-dbms/", "Tutorial", 3, "1NF, 2NF, 3NF and transitive dependency, B+ tree indexing and dirty read isolation levels.", "normalization 3nf transitive dependency b+ tree index dirty read"),
        ],
    },
    {
        "name": "Machine Learning",
        "icon": "🤖",
        "description": "Supervised and unsupervised learning, evaluation, regularization and ensembles.",
        "questions": [
            (1, "Which type of learning uses labelled training data?", ["Supervised learning", "Unsupervised learning", "Reinforcement learning", "Self-organised learning"], "Supervised models learn from input-output pairs."),
            (1, "Which of these is a classification algorithm?", ["Logistic Regression", "K-Means", "PCA", "Apriori"], "Despite its name, logistic regression predicts class labels."),
            (1, "What is overfitting?", ["Good on training data but poor on unseen data", "Poor on training and test data", "Training for too few epochs", "Using too little regularization on tests"], "An overfit model memorises noise instead of general patterns."),
            (2, "Which metric is most informative for an imbalanced classification problem?", ["F1-score", "Mean squared error", "R-squared", "Mean absolute error"], "F1 balances precision and recall so the minority class is not ignored."),
            (2, "What does K-Means do?", ["Partitions data into k clusters", "Predicts labels from examples", "Reduces dimensionality", "Builds decision trees"], "K-Means assigns points to the nearest of k centroids."),
            (2, "Why do we split data into train and test sets?", ["To evaluate generalisation on unseen data", "To increase dataset size", "To remove outliers", "To normalise features"], "The test set estimates performance on new data."),
            (3, "Which technique reduces dimensionality by maximising retained variance?", ["PCA", "k-NN", "SVM", "Naive Bayes"], "Principal Component Analysis projects data on high-variance directions."),
            (3, "What penalty does L2 regularization add to the loss?", ["Sum of squared weights", "Sum of absolute weights", "Number of features", "Largest weight"], "L2 (ridge) penalises the squared magnitude of weights."),
            (3, "What creates diversity among trees in a random forest?", ["Bootstrap samples and random feature subsets", "Identical data for every tree", "Gradient descent updates", "Pruning every tree to one split"], "Each tree sees a resampled dataset and a random subset of features."),
        ],
        "resources": [
            ("Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course", "Course", 1, "Supervised learning with labelled data, classification, logistic regression and overfitting basics.", "supervised labelled classification logistic regression overfitting"),
            ("Kaggle: Intro to Machine Learning", "https://www.kaggle.com/learn/intro-to-machine-learning", "Course", 1, "Train test split, model validation, overfitting and underfitting with decision trees.", "train test split validation overfitting underfitting decision tree"),
            ("scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html", "Documentation", 2, "K-means clustering, f1 score, precision recall and metrics for imbalanced classification.", "kmeans clustering f1 precision recall imbalanced metrics"),
            ("Ensemble Methods in scikit-learn", "https://scikit-learn.org/stable/modules/ensemble.html", "Documentation", 3, "Random forest bootstrap samples and feature subsets, PCA variance, L2 ridge regularization.", "random forest bootstrap pca variance l2 ridge regularization"),
        ],
    },
    {
        "name": "Web Development",
        "icon": "🌐",
        "description": "HTML, CSS, JavaScript, React and how the web communicates.",
        "questions": [
            (1, "Which HTML tag creates a hyperlink?", ["<a>", "<link>", "<href>", "<url>"], "The anchor tag with an href attribute creates links."),
            (1, "Which CSS property changes the colour of text?", ["color", "font-color", "text-style", "foreground"], "The color property sets the text colour."),
            (1, "Which language adds interactivity to web pages in the browser?", ["JavaScript", "SQL", "C", "Bash"], "JavaScript runs in the browser and manipulates the DOM."),
            (2, "What does HTTP status code 404 mean?", ["Not Found", "Internal Server Error", "Forbidden", "Created"], "404 means the requested resource does not exist."),
            (2, "Which React hook manages local component state?", ["useState", "useFetch", "useRoute", "useDom"], "useState returns a state value and its setter."),
            (2, "Which flexbox property aligns items along the main axis?", ["justify-content", "text-align", "float", "z-index"], "justify-content distributes items along the main axis."),
            (3, "What does CORS control?", ["Which origins may access resources across domains", "How passwords are hashed", "How CSS files are loaded", "How databases are queried"], "Cross-Origin Resource Sharing lets servers allow specific origins."),
            (3, "Which HTTP method is idempotent and replaces a whole resource?", ["PUT", "POST", "CONNECT", "TRACE"], "Repeating the same PUT leaves the resource in the same state."),
            (3, "What is the main purpose of the virtual DOM in React?", ["Minimise real DOM updates by diffing", "Store data on the server", "Compile JSX ahead of time", "Replace the browser engine"], "React diffs virtual trees and patches only what changed."),
        ],
        "resources": [
            ("MDN: Learn Web Development", "https://developer.mozilla.org/en-US/docs/Learn", "Documentation", 1, "HTML anchor tag hyperlink, CSS color property and JavaScript browser basics.", "html anchor hyperlink css color javascript"),
            ("HTML Tutorial", "https://www.w3schools.com/html/", "Tutorial", 1, "HTML tags and CSS text styles with try-it-yourself editor.", "html tags css text styles"),
            ("React: Learn", "https://react.dev/learn", "Documentation", 2, "React hooks, useState component state, flexbox justify-content layout and HTTP status codes like 404.", "react hooks usestate flexbox justify content http 404"),
            ("MDN: CORS", "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS", "Documentation", 3, "Cross origin resource sharing, REST PUT idempotent methods and React virtual DOM diffing.", "cors origin rest put idempotent virtual dom diffing"),
        ],
    },
]


def seed():
    if Topic.query.count() > 0:
        return
    for block in CONTENT:
        topic = Topic(name=block["name"], description=block["description"], icon=block["icon"])
        db.session.add(topic)
        db.session.flush()
        for index, (difficulty, text, options, explanation) in enumerate(block["questions"]):
            position = index % 4
            shuffled = list(options[1:])
            shuffled.insert(position, options[0])
            db.session.add(
                Question(
                    topic_id=topic.id,
                    text=text,
                    option_a=shuffled[0],
                    option_b=shuffled[1],
                    option_c=shuffled[2],
                    option_d=shuffled[3],
                    correct_option="ABCD"[position],
                    difficulty=difficulty,
                    explanation=explanation,
                )
            )
        for title, url, kind, level, description, tags in block["resources"]:
            db.session.add(
                Resource(
                    topic_id=topic.id,
                    title=title,
                    url=url,
                    kind=kind,
                    level=level,
                    description=description,
                    tags=tags,
                )
            )
    db.session.commit()
