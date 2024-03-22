```mermaid
graph TD
    subgraph <u>Manuscript</u>
    A[Manuscript] --> B[Draft]
    end

    subgraph poster
    C[Poster] --> D[Draft]
    end

    subgraph presentation
    E[Presentation] --> F[Draft]
    end

    subgraph <u>Grant</u>
        subgraph "Science"
        direction TB
        a[<ul><li>Specific Aims<li>Research Strategy</ul>]:::macList
        end

        subgraph "Administrative"
        direction TB
        a[<ul><li>Budget<li>Budget Justification<li>Biosketches<li>Facilities</ul>]:::macList
        end

        subgraph marketing
        direction TB
        a[<ul><li>Significance<li>Impact</ul>]:::macList
        end
    end

   classDef macList text-align:left;
```
