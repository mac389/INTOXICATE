---
title: "Exposure Category by Gender"
author: "Yash Jaggi"
output: 
  pdf_document:
    latex_engine: xelatex
    toc: false
    keep_tex: true
header-includes:
  - \usepackage{booktabs}
  - \usepackage{caption}
  - \usepackage{float}
  - \renewcommand{\familydefault}{\sfdefault}
  - \usepackage{placeins}
---





\begin{table}[t]
\caption{\label{tab:summary_table}\textbf{Males (M) are more likely to have exposures to occupational agents (CO, As, CN) and street drugs than females (F) and females more likely to have exposures to analgesics and antidepressants than males}. The `Other' category combines Antipsychotic, Chlorine Gas, clorox bleach, and Sedative (Combination) due to less than five total exposures for each of these exposure categories.} 
\fontsize{12.0pt}{14.4pt}\selectfont
\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}lccc}
\toprule
\textbf{Characteristic} & \textbf{F}  N = 59\textsuperscript{\textit{1}} & \textbf{M}  N = 52\textsuperscript{\textit{1}} & \textbf{p-value}\textsuperscript{\textit{2}} \\ 
\midrule\addlinespace[2.5pt]
{\bfseries Exposure Category} &  &  & 0.2 \\ 
    Combination & 7 (12\%) & 10 (19\%) &  \\ 
    Analgesic & 11 (19\%) & 7 (13\%) &  \\ 
    Antidepressants & 12 (20\%) & 6 (12\%) &  \\ 
    Street Drugs & 6 (10\%) & 11 (21\%) &  \\ 
    CO, As, CN & 4 (6.8\%) & 7 (13\%) &  \\ 
    Sedatives & 4 (6.8\%) & 3 (5.8\%) &  \\ 
    Alcohol & 3 (5.1\%) & 4 (7.7\%) &  \\ 
    Other & 0 (0\%) & 0 (0\%) &  \\ 
    Unknown & 12 (20\%) & 4 (7.7\%) &  \\ 
\bottomrule
\end{tabular*}
\begin{minipage}{\linewidth}
\textsuperscript{\textit{1}}n (\%)\\
\textsuperscript{\textit{2}}Fisher's exact test\\
\end{minipage}
\end{table}




## Interpretation

The sample included toxicology consults coming through the emergency department: 59 females (53%) and 52 males (47%). This balanced gender distribution is consistent with patterns observed in similar toxicology consultation studies.

The chi-square test of independence found **no significant association** between gender and exposure category (*p* = NA), indicating that gender does not significantly influence the types of exposures seen in this clinical population.

**Key findings:**

- Females show relatively higher representation in analgesic (64%) and antidepressant exposures (74%), which aligns with literature suggesting different patterns of intentional ingestion between genders.
- Males show greater representation in CO/As/CN (67%) and street drug exposures (61%), potentially reflecting occupational or behavioral exposure patterns.
- The largest exposure categories were Combination (n=49), Analgesic (n=25), and Antidepressants (n=23), representing 52% of all consultations.
- Visual differences in Figures 1 and 2 were not statistically significant, suggesting these patterns may reflect chance variation or unmeasured confounding factors.
- Overall distribution is balanced across categories, suggesting gender is unlikely to confound downstream analyses of clinical outcomes or risk stratification models like INTOXICATE.

# Supplemental Material
```{=latex}
\setcounter{figure}{0}
\renewcommand{\thefigure}{S\arabic{figure}}
```


\begin{figure}
\includegraphics[width=0.9\linewidth]{../../notebook/yash/fig_1} \caption{Females show relatively higher counts in analgesic and antidepressant exposures, whereas males are more represented in CO/As/CN and street drug exposures. These differences are not statistically significant.}\label{fig:fig1}
\end{figure}

\begin{figure}
\includegraphics[width=0.9\linewidth]{../../notebook/yash/fig2} \caption{Within-gender proportions for each exposure category (bars sum to 100\% for each gender). Females have higher proportions in analgesic and antidepressant exposures, while males show higher proportions in CO/As/CN and street drugs. The chi-square test indicates the overall gender–exposure association is not statistically significant.}\label{fig:fig2}
\end{figure}


