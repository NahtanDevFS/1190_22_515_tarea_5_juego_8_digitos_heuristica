Jonathan David Franco Sosa 1190-22-515 Curso: inteligencia artificial

Tarea 5: Agente inteligente capaz de resolver el juego de 8 dígitos mediante reglas heurísticas usando el algoritmo A*.

El Algoritmo A* es un algoritmo informado, es decir, en lugar de explorar todo el árbol de posibilidades mediante fuerza bruta como lo hace el algoritmo BFS, 
este evalúa cada tablero posible y le asigna un costo usando la fórmula: f(n) = g(n) + h(n)
<br>

g(n) (costo real): Es la cantidad exacta de movimientos que el agente ha hecho desde el tablero inicial para llegar al tablero actual, si hizo 5 movimientos, g(n) es 5
<br>

h(n) (costo heurístico): Es una estimación de cuántos movimientos faltan para llegar a la meta que se conoce como Distancia de Manhattan que calcula cuántas casillas horizontales 
y verticales tendría que moverse cada ficha desde donde está ahora hasta donde debería estar en el objetivo, si se debe mover 4 casillas, entonces el valor de h(n) es 4
<br>

f(n) (costo total estimado): Es la suma de ambos, el algoritmo siempre va a sacar de la la cola de prioridad el tablero que tenga el f(n) más bajo, porque representa el camino más eficiente
<br>

Es así que mediante este algoritmo buscará siempre la ruta más óptima, ya que buscará siempre la que proporcione una f(n) de menor coste
<br>
<br>
Para este ejemplo:
<br>
<img width="246" height="233" alt="image" src="https://github.com/user-attachments/assets/ff215b62-f547-4f61-8622-4aca920e038e" />
<br>
<img width="395" height="583" alt="image" src="https://github.com/user-attachments/assets/fb43debb-d63e-466c-873b-feb07aaa9802" />
<br>
Al evaluarse mediante el algoritmo A*, se obtiene que se resolvió evaluando 2,491 nodos, aunque parezcan muchos, con el algoritmo BFS, resolver este 
ejemplo le tomaría evaluar alrededor de 150,000 nodos, es decir, hay una enorme reducción en los pasos al resolverlo con reglas heurísticas
<br>
<img width="393" height="581" alt="image" src="https://github.com/user-attachments/assets/2036767c-6d8f-4482-ad47-ceb347ae5f0a" />
<br>
Ejercicio resuelto:
<br>
<img width="388" height="575" alt="image" src="https://github.com/user-attachments/assets/e271329f-ebf1-4c70-bc2b-c7495892e111" />
<br>
<br>
Por ejemplo, este otro ejercicio:
<br>
<img width="230" height="227" alt="image" src="https://github.com/user-attachments/assets/b4867aa1-0fef-45b1-b7f6-2427cfee961d" />
<br>
<img width="390" height="565" alt="image" src="https://github.com/user-attachments/assets/47a9b543-c606-43a9-a458-7e1a2949fe28" />
<br>
Mediante el algoritmo A* se evaluaron solamente 6 nodos, muchos menos de los que serían necesarios con el algoritmo BFS
<br>
<img width="395" height="571" alt="image" src="https://github.com/user-attachments/assets/1920faa2-8c6b-4371-933f-b62d075fc0b1" />
<br>
Ejercicio resuelto:
<br>
<img width="394" height="585" alt="image" src="https://github.com/user-attachments/assets/a7693332-0657-49a8-821b-3d4a8aa61777" />
<br>
<br>
Nota: El archivo requirements.txt está vacío, ya que las librerías utilizadas son propias de Python, así que no se necesita instalar nada para ejecutar el proyecto.




