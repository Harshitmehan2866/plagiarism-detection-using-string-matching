flowchart TD
    A([Start]) --> B[/Upload or enter Document A and B/]
    B --> C{Both documents provided?}
    C -- No --> D[Display warning]
    D --> B
    C -- Yes --> E[Normalize document text]
    E --> F[Extract unique five-word patterns]
    F --> G[Run Naive, KMP, Rabin-Karp and Boyer-Moore]
    G --> H[Record match positions and comparisons]
    H --> I[Measure execution time]
    I --> J[Find shared five-word passages]
    J --> K[Highlight matching passages]
    K --> L[Display results table and graphs]
    L --> M([End])