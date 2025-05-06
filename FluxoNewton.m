0%% FLUXO DE POT�NCIA MONOF�SICO ATRAV�S DO M�TODO DE INJE��O DE POT�NCIAS TRADICIONAL


clearvars -except aux1 aux2 jjj iii Class ss1 ss2 swd

%        |Barra | Tipo| Vo | Thetao | Pg | Qg |  Pd |   Qd |    Qmin |    Qmax |
busd = [    1     1    1.000   0       0    0    0       0        0        0;
            2     3    1.000   0      40   23   240.0   120.0   -9999     9999;
            3     3    aux1   aux2    40   23   240.0   120.0   -9999     9999;
            ];


%         |  De |  Para   |   R(pu)  |   X(pu) |  B/2 (pu) |   a  |
linedata =  [1      2       0.01938   0.05917    0.00264       1
             1      3       0.05403   0.22304    0.00246       1
             2      3       0.04699   0.19797    0.00219       1 
            ];

%% Etapa 1) Leitura dos dados de ramos:

fb = linedata(:,1);         % barra DE
tb = linedata(:,2);         % barra PARA
nb = max(max(fb),max(tb));  % n�mero de barras
nl = length(fb);            % n�mero de ramos


r = linedata(:,3);      % resist�ncia
x = linedata(:,4);      % reat�ncia
b = linedata(:,5);      % admit�ncia shunt
a = linedata(:,6);      % valor de tap
z = r + i*x;            % Imped�ncias dos trechos
y = 1./z;               % Admit�ncias dos trechos
b = i*b;                % Compatibilizando b imagin�rio


%% Etapa 2) Forma��o da matriz de admit�ncia nodal

Y = zeros(nb,nb);        % Forma��o da matriz de admit�ncia nodal
 
 % Elementos fora da diagonal
 for k = 1:nl
     Y(fb(k),tb(k)) = Y(fb(k),tb(k)) - y(k)/a(k);
     Y(tb(k),fb(k)) = Y(fb(k),tb(k));
 end
 
 % Elementos da diagonal
 for m = 1:nb
     for n = 1:nl
         if fb(n) == m
             Y(m,m) = Y(m,m) + y(n)/(a(n)^2) + b(n);
         elseif tb(n) == m
             Y(m,m) = Y(m,m) + y(n) + b(n);
         end
     end
 end
 Y;                  % Matriz de admit�ncias
 Zbuz = inv(Y);      % Matriz de imped�ncias nodais
G = real(Y);                % Matriz de Condut�ncias
B = imag(Y);                % Matriz de Suscept�ncias

%% Leitura de dados de barra:
BMva = 1000;                % Pot�ncia base
bus = busd(:,1);            % N�mero da barra
type = busd(:,2);           % Tipo da barra: 1-Refer�ncia, 2-PV, 3-PQ.
V = busd(:,3);              % Tens�es especificadas
del = busd(:,4);            % �ngulos de fase
Pg = busd(:,5)/BMva;        % Pot�ncia Ativa gerada
Qg = busd(:,6)/BMva;        % Pot�ncia Reativa gerada
Pl = busd(:,7)/BMva;        % POt�ncia ativa demandada
Ql = busd(:,8)/BMva;        % Pot�ncia reativa demandada
Qmin = busd(:,9)/BMva;      % Limite m�nimo de reativos
Qmax = busd(:,10)/BMva;     % Limite m�ximo de reativos
nbus = max(bus);            % N�mero total de barras
P = Pg - swd*Pl;            % Pot�ncia liquida ativa
Q = Qg - swd*Ql;            % Pot�ncia liquida reativa 
Psp = P;                    % Pot�ncia ativa especificada      
Qsp = Q;                    % Pot�ncia reativa especificada


pv = find(type == 2 | type == 1);       % Indice de barras PV
npv = length(pv);                       % Numero de barras PV
pq = find(type == 3);                   % Indice de barras PQ
npq = length(pq);                       % Numero de barras PQ

%% Etapa 3) Processo iterativo de Newton-Raphson
Tol = 1;            % vari�vel de toler�ncia
Iter = 1;           % vari�vel contadora de itera��es

while (Tol > 1e-8) && Iter <= 20   % in�cio do processo iterativo
    P = zeros(nbus,1);
    Q = zeros(nbus,1);
    % Calcular P and Q funcionais
    for i = 1:nbus
        for k = 1:nbus
            P(i) = P(i) + V(i)* V(k)*(G(i,k)*cos(del(i)-del(k)) + B(i,k)*sin(del(i)-del(k)));
            Q(i) = Q(i) + V(i)* V(k)*(G(i,k)*sin(del(i)-del(k)) - B(i,k)*cos(del(i)-del(k)));
        end
    end


    % Calcular res�duos de pot�ncias
    dPa = Psp-P;
    dQa = Qsp-Q;
    k = 1;
    dQ = zeros(npq,1);
    for i = 1:nbus
        if type(i) == 3
            dQ(k,1) = dQa(i);
            k = k+1;
        end
    end
    dP = dPa(2:nbus);
    M = [dP; dQ];       % Vetor de res�duos
    
    % Jacobiana
    % J1 - Derivadas parciais de P em rela��o a angulos 
    J1 = zeros(nbus-1,nbus-1);
    for i = 1:(nbus-1)
        m = i+1;
        for k = 1:(nbus-1)
            n = k+1;
            if n == m
                for n = 1:nbus
                    J1(i,k) = J1(i,k) + V(m)* V(n)*(-G(m,n)*sin(del(m)-del(n)) + B(m,n)*cos(del(m)-del(n)));
                end
                J1(i,k) = J1(i,k) - V(m)^2*B(m,m);
            else
                J1(i,k) = V(m)* V(n)*(G(m,n)*sin(del(m)-del(n)) - B(m,n)*cos(del(m)-del(n)));
            end
        end
    end
    
    % J2 - Derivadas parciais de P em rela��o a V 
    J2 = zeros(nbus-1,npq);
    for i = 1:(nbus-1)
        m = i+1;
        for k = 1:npq
            n = pq(k);
            if n == m
                for n = 1:nbus
                    J2(i,k) = J2(i,k) + V(n)*(G(m,n)*cos(del(m)-del(n)) + B(m,n)*sin(del(m)-del(n)));
                end
                J2(i,k) = J2(i,k) + V(m)*G(m,m);
            else
                J2(i,k) = V(m)*(G(m,n)*cos(del(m)-del(n)) + B(m,n)*sin(del(m)-del(n)));
            end
        end
    end
    
    % J3 - Derivadas parciais de Q em rela��o a angulos 
    J3 = zeros(npq,nbus-1);
    for i = 1:npq
        m = pq(i);
        for k = 1:(nbus-1)
            n = k+1;
            if n == m
                for n = 1:nbus
                    J3(i,k) = J3(i,k) + V(m)* V(n)*(G(m,n)*cos(del(m)-del(n)) + B(m,n)*sin(del(m)-del(n)));
                end
                J3(i,k) = J3(i,k) - V(m)^2*G(m,m);
            else
                J3(i,k) = V(m)* V(n)*(-G(m,n)*cos(del(m)-del(n)) - B(m,n)*sin(del(m)-del(n)));
            end
        end
    end
    
    % J4 - Derivadas parciais de Q em rela��o a V 
    J4 = zeros(npq,npq);
    for i = 1:npq
        m = pq(i);
        for k = 1:npq
            n = pq(k);
            if n == m
                for n = 1:nbus
                    J4(i,k) = J4(i,k) + V(n)*(G(m,n)*sin(del(m)-del(n)) - B(m,n)*cos(del(m)-del(n)));
                end
                J4(i,k) = J4(i,k) - V(m)*B(m,m);
            else
                J4(i,k) = V(m)*(G(m,n)*sin(del(m)-del(n)) - B(m,n)*cos(del(m)-del(n)));
            end
        end
    end
    
    J = [J1 J2; J3 J4];         % Matriz Jacobiana
    X = J\M;                    % Defini��o do vetor X de res�duos de V e angulos
    dTh = X(1:nbus-1);          % Residuos de angulos
    dV = X(nbus:end);           % Residuos de tens�es V
    
    % Atualiza��o do vetpr solu��o:
    del(2:nbus) = dTh + del(2:nbus);
    k = 1;
    for i = 2:nbus
        if type(i) == 3
            V(i) = dV(k) + V(i);
            k = k+1;
        end
    end
    Iter = Iter + 1;           % pr�xima itera��o
    Tol = max(abs(M));         % c�lculo de toler�ncia
end

   
% Final do processo iterativo

num=nb;

Vm = V.*(cos(del)+j*sin(del));      % Obten��o dos valores de tens�o complexos
Del = 180/pi*del;                   % Angulos dem graus
fb = linedata(:,1);            % barra DE
tb = linedata(:,2);            % barra PARA
b = linedata(:,5);             % B shunt
a = linedata(:,6);             % tap
nl = length(fb);            % n�mero de ramos
Pl = busd(:,7);             % pot�ncia ativa de carga
Ql = busd(:,8);             % pot�ncia reativa de carga

nb = length(Vm);            % Numero de barras
Iij = zeros(nb,nb);         % correntes ramais
Sij = zeros(nb,nb);         % fluxos complexos

% INje��es de correntes nas barras do sistema
 I = Y*Vm;
 Im = abs(I);
 Ia = angle(I);
 
%Fluxos de correntes nas linhas
 for m = 1:nb
     for n = 1:nl
         if fb(n) == m
             p = tb(n);
             Iij(m,p) = -(Vm(m) - Vm(p)*a(n))*Y(m,p)/a(n)^2 + b(n)/a(n)^2*Vm(m);  
             Iij(p,m) = -(Vm(p) - Vm(m)/a(n))*Y(p,m) + b(n)*Vm(p);
         elseif tb(n) == m
             p = fb(n);
             Iij(m,p) = -(Vm(m) - Vm(p)/a(n))*Y(p,m) + b(n)*Vm(m);
             Iij(p,m) = -(Vm(p) - Vm(m))*Y(m,p)/a(n)^2 + b(n)/a(n)^2*Vm(p);
         end
     end
 end
 
 Iijr = real(Iij);
 Iiji = imag(Iij);

 % Fluxos de pot�ncias
 for m = 1:nb
     for n = 1:nb
         if m ~= n
             Sij(m,n) = Vm(m)*conj(Iij(m,n))*BMva;
         end
     end
 end
 
 Pij = real(Sij);
 Qij = imag(Sij);
 
 % Perdas nas linhas:
 Lij = zeros(nl,1);
 for m = 1:nl
     p = fb(m); q = tb(m);
     Lij(m) = Sij(p,q) + Sij(q,p);
 end
 
 Lpij = real(Lij);
 Lqij = imag(Lij);
 
 % Pot�ncias injetadas em cada barra
 Si = zeros(nb,1);
 
 for i = 1:nb
     for k = 1:nb
         Si(i) = Si(i) + conj(Vm(i))* Vm(k)*Y(i,k)*BMva;
     end
 end
 Pi = real(Si);
 Qi = -imag(Si);
 Pg = Pi+Pl;    % pot�ncias geradas
 Qg = Qi+Ql;    % pot�ncias reativas geradas
 
 [V Del];
 
 x = eig(J);
 aaaa = 0;
  
  for hhh = 1:length(x)
     if real(x(hhh)) < 0.6
         aaaa = aaaa+1;
     end
 end
 
 
 if Iter >= 20
     class = 4; %Branco Esp�ria
 else
     
     if aaaa == 0
        class = 1; %Azul Est�vel

     elseif aaaa == 1
         class = 2; %Amarelo Tipo1

     else
         class = 3; %Verde Tipo2
     end
 end
 
 eig(J); 
 

 
