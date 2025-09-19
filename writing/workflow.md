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
    Sci[<u>Science</u><ul><li>Specific Aims<li>Research Strategy</ul>]:::macList ~~~ Admin[<u>Admin</u><ul><li>Budget<li>Budget Justification<li>Biosketches<li>Facilities</ul>]:::macList ~~~ Marketing[<u>Marketing</u><ul><li>Significance<li>Impact</ul>]:::macList

        click Sci "./sop/grants/"
        click Admin "./sop/grants/"
        click Marketing "./sop/grants/"
    end

   classDef macList text-align:left;
```
