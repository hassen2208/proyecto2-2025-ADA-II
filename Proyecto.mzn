include "globals.mzn";

%----------------------------------- Parámetros -----------------------------------

int: n;                           % Número total de personas
int: m;                           % Número de posibles opiniones
array[1..m] of int: p;            % Distribución inicial de personas por opinión
array[1..m] of float: v;          % Valor de extremismo asociado a cada opinión
array[1..m, 1..m] of float: c;    % Matriz de costos de cambio entre opiniones
array[1..m] of float: ce;         % Costos adicionales para opiniones inicialmente vacías
float: ct;                        % Costo total máximo permitido
int: maxM;                        % Número máximo de movimientos permitidos

%----------------------------------- Variables -----------------------------------

array[1..m, 1..m] of var 0..n: x;     % x[i,j]: Personas que se mueven de opinión i a j
array[1..m] of var 0..n: p_new;       % Nueva distribución final por opinión
var float: Z;                         % Extremismo total (función objetivo)

%----------------------------------- Precálculos -----------------------------------

array[1..m] of float: factor = [1.0 + p[i] / n | i in 1..m];

array[1..m, 1..m] of float: cost_per_person = array2d(1..m, 1..m, 
    [ c[i, j] * factor[i] + (if p[j] = 0 then ce[j] else 0.0 endif) | i in 1..m, j in 1..m ]);

%----------------------------------- Restricciones -----------------------------------

% 1. Nadie se mueve a la misma opinión
constraint forall(i in 1..m)(
    x[i, i] = 0
);

% 2. No mover más personas de las que hay en cada opinión
constraint forall(i in 1..m)(
    sum(j in 1..m)(x[i, j]) <= p[i]
);

% 3. Nueva distribución final por opinión
constraint forall(i in 1..m)(
    p_new[i] = p[i] + sum(j in 1..m)(x[j, i] - x[i, j])
);

% 4. Costo total no puede superar el permitido
constraint sum(i in 1..m, j in 1..m)(
    cost_per_person[i, j] * int2float(x[i, j])
) <= ct;

% 5. Número de movimientos permitidos
constraint sum(i in 1..m, j in 1..m)(
    abs(i - j) * x[i, j]
) <= maxM;

% 6. Conservar el total de personas
constraint sum(i in 1..m)(p_new[i]) = n;

% 7. Limitar cantidad de movimientos posibles
constraint forall(i in 1..m, j in 1..m)(
    x[i, j] <= p[i]
);

%----------------------------------- Función Objetivo -----------------------------------

constraint Z = sum(i in 1..m)(p_new[i] * v[i]);
solve minimize Z;

%----------------------------------- Salida -----------------------------------

output [
    "Extremismo total: ", show(Z), "\n",
    "Nueva distribución de opiniones: ", show(p_new), "\n",
    "Distribución de movimientos (x): ", show(x), "\n",
];
