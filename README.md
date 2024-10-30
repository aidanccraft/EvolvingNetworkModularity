# EvolvingNetworkModularity
Modularity is a common feature in biological networks, wherein individual parts of the network function as a single larger unit within the overall system. These units are often responsible for simple tasks like response to a single stimulus or set of related stimuli, and interface with other modules to result in the functionality of the network as a whole. Due to the prevalence of modules within biological networks, it is readily apparent that they are advantageous to the performance of such networks, however the exact reasons for this advantage are unclear.

In the process of investigating this and other features of biological networks, computational evolution of neural networks and similar systems have been used, but this process generally results in networks which do not exhibit modularity and have tangled, unintuitive topologies. The use of changing goals which share common constitutive tasks has successfully produced modular networks, and a connection between this approach and real conditions can be justified.

In addition to insights about biological evolution, understanding the evolution of and driving forces towards modularity within networks could prove beneficial for the creation and understanding of complex neural networks used in applications like machine learning and artificial intelligence. The ability to influence and/or predict the evolution of networks based on their goals could be integral to solving the ‘black box problem’ of artificial intelligence, especially as modularity can simplify understanding and analysis of a network and improve the breadth of tasks for which the network is appropriate.

## Project Details
This project was completed by <a href=https://github.com/aidanccraft>@aidanccraft</a> and <a href=https://github.com/gwstrain>@gwstrain</a> as the final project for our Systems Biology class at Colorado School of Mines. The goal was to recreate and expand upon the results of <a href="https://www.pnas.org/doi/10.1073/pnas.0503610102">Kashtan et al.</a> Networks were evolved using four binary inputs and genes encoding NAND gates. These networks were evolved under fixed and modularly varying goals represented by logic statements: 

$$\begin{align*}
    G_1&=({\mathrm{X}}\ {\ }\ {\mathrm{XOR}}\ {\ }\ {\mathrm{Y}})\ {\ }\ {\mathrm{AND}}\ {\ }\ ({\mathrm{Z}}\ {\ }\ {\mathrm{XOR}}\ {\ }\ {\mathrm{W}}), \\
    G_2&=({\mathrm{X}}\ {\ }\ {\mathrm{XOR}}\ {\ }\ {\mathrm{Y}})\ {\ }\ \ {\mathrm{OR}}\ {\ }\ \ \ ({\mathrm{Z}}\ {\ }\ {\mathrm{XOR}}\ {\ }\ {\mathrm{W}}).
\end{align*}$$

These goals were swapped every 20 generations to promote the formation of modularity in the networks. Examples of modularly evolved networks under these goals can be seen below:

<div align="center">
 <img src="https://github.com/user-attachments/assets/50507695-c4cb-4ab8-864a-1c0d8140ac94" width="500"/>
</div>

These simulations were able to find optimal solutions in less than 10,000 generations which could quickly switch between goals. This indicates that modularly varying goals are a potential method to evolve modular networks in real biological systems.

Simulations and analysis were done in Python with multiprocessing to speed up the genetic algorithm. The results for this project were communicated via a [report](https://github.com/user-attachments/files/17576377/BIOL520_FinalReport.pdf) and a [presentation](https://github.com/user-attachments/files/17576390/BIOL520_FinalPresentation.pdf).

