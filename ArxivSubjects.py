""" This file is just for convenience.  Holds all the hardcoded subjects and subcategories from arxiv. """

subject_list = ['physics:astro-ph','physics:cond-mat','physics:gr-qc',
                'physics:hep-ex','physics:hep-lat','physics:hep-ph','physics:hep-th',
                'physics:math-ph','physics:nlin','physics:nucl-ex','physics:nucl-th',
                'physics','physics:quant-ph','math','cs','q-bio','q-fin','stat']

math = ['Algebraic Geometry','Algebraic Topology','Analysis of PDEs','Category Theory',
        'Classical Analysis and ODEs','Combinatorics','Commutative Algebra',
        'Complex Variables','Differential Geometry','Dynamical Systems','Functional Analysis',
        'General Mathematics','General Topology','Geometric Topology','Group Theory',
        'History and Overview','Information Theory','K-Theory and Homology','Logic',
        'Mathematical Physics','Metric Geometry','Number Theory','Numerical Analysis',
        'Operator Algebras','Optimization and Control','Probability','Quantum Algebra',
        'Representation Theory','Rings and Algebras','Spectral Theory','Statistics Theory',
        'Symplectic Geometry']

physics = ['Accelerator Physics','Atmospheric and Oceanic Physics','Atomic Physics',
        'Atomic and Molecular Clusters','Biological Physics','Chemical Physics','Classical Physics',
        'Computational Physics','Data Analysis, Statistics and Probability','Fluid Dynamics',
        'General Physics','Geophysics','History and Philosophy of Physics',
        'Instrumentation and Detectors','Medical Physics','Optics','Physics Education',
        'Physics and Society','Plasma Physics','Popular Physics','Space Physics']

astroph = ['Astrophysics of Galaxies','Cosmology and Nongalactic Astrophysics',
        'Earth and Planetary Astrophysics','High Energy Astrophysical Phenomena',
        'Instrumentation and Methods for Astrophysics','Solar and Stellar Astrophysics']

cond_mat = ['Disordered Systems and Neural Networks','Materials Science',
            'Mesoscale and Nanoscale Physics','Other Condensed Matter','Quantum Gases',
            'Soft Condensed Matter','Statistical Mechanics','Strongly Correlated Electrons',
            'Superconductivity']

nlin_sci = ['Adaptation and Self-Organizing Systems','Cellular Automata and Lattice Gases',
            'Chaotic Dynamics','Exactly Solvable and Integrable Systems','Pattern Formation and Solitons']

cs = ['Artificial Intelligence','Computation and Language',
      'Computational Complexity','Computational Engineering, Finance, and Science',
      'Computational Geometry','Computer Science and Game Theory',
      'Computer Vision and Pattern Recognition','Computers and Society',
      'Cryptography and Security','Data Structures and Algorithms','Databases',
      'Digital Libraries','Discrete Mathematics','Distributed, Parallel, and Cluster Computing',
      'Emerging Technologies','Formal Languages and Automata Theory','General Literature',
      'Graphics','Hardware Architecture','Human-Computer Interaction','Information Retrieval',
      'Information Theory','Learning','Logic in Computer Science','Mathematical Software',
      'Multiagent Systems','Multimedia','Networking and Internet Architecture',
      'Neural and Evolutionary Computing','Numerical Analysis','Operating Systems',
      'Other Computer Science','Performance','Programming Languages','Robotics',
      'Social and Information Networks','Software Engineering','Sound','Symbolic Computation',
      'Systems and Control']

q_bio = ['Biomolecules','Cell Behavior','Genomics','Molecular Networks',
         'Neurons and Cognition','Other Quantitative Biology','Populations and Evolution',
         'Quantitative Methods','Subcellular Processes','Tissues and Organs']

q_fin = ['Computational Finance','Economics','General Finance','Mathematical Finance',
         'Portfolio Management','Pricing of Securities','Risk Management','Statistical Finance',
         'Trading and Market Microstructure']

stat = ['Applications','Computation','Machine Learning','Methodology',
        'Other Statistics','Statistics Theory']

subject_dict = {'physics:astro-ph':astroph,'physics:cond-mat':cond_mat,
                'physics:gr-qc':[],'physics:hep-ex':[],'physics:hep-lat':[],'physics:hep-ph':[],
                'physics:hep-th':[],'physics:math-ph':[],'physics:nlin':nlin_sci,'physics:nucl-ex':[],
                'physics:nucl-th':[],'physics':physics,'physics:quant-ph':[],'math':math,'cs':cs,
                'q-bio':q_bio,'q-fin':q_fin,'stat':stat}

subject_name = {'physics:astro-ph':'Astrophysics','physics:cond-mat':'Condensed Matter',
                'physics:gr-qc':'General Relativity and Quantum Cosmology',
                'physics:hep-ex':'High Energy Physics - Experiment',
                'physics:hep-lat':'High Energy Physics - Lattice',
                'physics:hep-ph':'High Energy Physics - Phenomenology',
                'physics:hep-th':'High Energy Physics - Theory','physics:math-ph':'Mathematical Physics',
                'physics:nlin':'Nonlinear Sciences','physics:nucl-ex':'Nuclear Experiment',
                'physics:nucl-th':'Nuclear Theory','physics':'Physics',
                'physics:quant-ph':'Quantum Physics','math':'Mathematics','cs':'Computer Science',
                'q-bio':'Quantitative Biology','q-fin':'Quantitative Finance','stat':'Statistics'}
