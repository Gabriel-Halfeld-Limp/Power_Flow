
% +---------------------------------------------------------------------------------------+
%                                  FLUXO DE POT�NCIA
%                               (Coordenada retangular)
%                                =====================
% +---------------------------------------------------------------------------------------+

clear all
close all
warning 'off'


%==============================================================================================================
%                                                                            S�rie     Paralelo
%   Barra  Tipo   V[pu] teta[�]   PG[MW]     Qg[MVar]     PD[MW]     QD[MVar] Bsh[MVar] Bsh[MVar]  Qmin  Qmax
%     1      2       3     4        5            6           7            8       9        10       11   12
%===============================================================================================================
barras=[ 1      2     1      0        0          0           0.0           0       0        0        0     0
         2      0     1.00   0        0          0            5            2       0        0     -999    999
         3      1     0.98   0        0          0           15            0       0        0        0     0   ];

%--------------------------------
% Tipo: 0 - Barra PQ
%       1 - Barra PV
%       2 - Barra ref

%=================================================================================================
%         DE   PARA      R[pu]     X[pu]        Sh[pu]      Tap    Tap(min)  Tap(max)
%         1     2         3         4             5          6       7         8
%=================================================================================================
linhas = [1     2        0.10       1.00         0.01*2        0      0        0
          1     3        0.20       2.00         0.02*2        0        0        0
          2     3        0.10       1.00         0.01*2        0        0        0         ];
%-------------------------------------------------------------------------------------------------

%-----------------
% LEITURA DE DADOS
%-----------------
pb=100;
t0 = clock;                % t0 --> tempo inicial de processamento.

n       = size(barras,1);  % N�mero de barras do sistema = n�mero de linhas.
nlinhas = size(linhas,1);  % N�mero de linhas da matriz linhas.
Y       = zeros(n);        % Y --> matriz admit�ncia, quadrada de ordem nlinhas.
ngen = numel(find(barras(:,2)==1)); % N�mero de barras PV
tolera = 1e-4;             % Toler�ncia do m�todo de Newton Raphson

V  = barras(:,3);
O  = barras(:,4).*(pi/180);
P  = (barras(:,5)-barras(:,7))/pb;
Q  = (barras(:,6)-barras(:,8))/pb;
pger = barras(:,5)./pb;
qger = zeros(n,1);
Pd = barras(:,7)./pb;
Qd = barras(:,8)./pb;
Pesp = pger - Pd;
Qesp = qger - Qd;

[xx,yy] = pol2cart(O*pi/180,V);
Vret = xx + 1i*yy;
Iret = Y*Vret;
Ir = real(Iret);          %Correntes reais
Im = imag(Iret);         %Correntes imaginarias
Vr = real(Vret);
Vm = imag(Vret);

% Inicializa��es
dPQ(2*n,1)    = 0;
dOV(2*n,1)    = 0;
PQcalc(2*n,1) = 0;
barras_ligadas = zeros(n+1);
barras_pv = find(barras(:,2) == 1);

nsht = 0;                  % Contador do n�mero de shunts em barra
ntrafos = 0;               % Contador do numero de trafos

VrVm = [Vr ; Vm];

% ------------------------------
% Forma��o da Matriz Admit�ncia
% ------------------------------

for k = 1:n
    Y(k,k) = Y(k,k) + (barras(k,9) + 1i*barras(k,10))/pb;
end

for s = 1:nlinhas
    ntap(s) = 0;
    r = linhas(s,3);
    x = linhas(s,4);
    blin = linhas(s,5)*0.5;    % Shunt de Linha
    
    if ((linhas(s,6) ~= 0) && (linhas(s,6) ~= 1)) % Se tap diferente de 0 e de 1,
        ntrafos = ntrafos + 1;     % Contador do numero de trafos
        notap(ntrafos) = s;
        ntap(s) = ntrafos;
        a = 1/linhas(s,6); % a = 1/tap
        tap(ntrafos) = a;                  % Valor do Tap do transformador
        aa(ntrafos)=0;
        troca_cont(ntrafos) = 0;
        cont(ntrafos) = 0;
    else
        a = 1;
    end
    y = 1/(r + x*1i);
    gkm(s) = real(y);       % Condut�ncia da Linha
    bkm(s) = imag(y);       % Suscept�ncia da Linha
    
    k = find(barras(:,1) == linhas(s,1));
    m = find(barras(:,1) == linhas(s,2));
    Y(k,m) = Y(k,m) - a*(1/(linhas(s,3)+1i*linhas(s,4))); % tap => Influ�ncia do trafo.
    Y(m,k) = Y(k,m); % Pois a matriz � sim�trica.
    Y(k,k) = Y(k,k) + a^2*(1/(linhas(s,3)+1i*linhas(s,4))) + 1i*linhas(s,5)/2;
    Y(m,m) = Y(m,m) + (1/(linhas(s,3)+1i*linhas(s,4))) + 1i*linhas(s,5)/2;
end
G = real(Y);
B = imag(Y);
aux=0;

for k = 1:n
    barras_k   = find(Y(k,:) ~= 0); % Guarda em barras_k as barras ligadas � barra k.
    num_barras = size(barras_k,2);  % N�mero de colunas = n�mero de barras ligadas � barra k.
    barras_ligadas(k,1:num_barras) = barras_k;
    barras_ligadas(k,n+1)          = num_barras;
    
    for m = 1:barras_ligadas(k,n+1)
        %C�lculo de Pk
        PQcalc(k,1)   = PQcalc(k,1) + ...
            Vr(k)*(Vr(m)*G(k,m) - Vm(m)*B(k,m)) + Vm(k)*(Vm(m)*G(k,m)+Vr(m)*B(k,m));
        %C�lculo de Qk
        PQcalc(k+n,1) = PQcalc(k+n,1) + ...
            Vm(k)*(Vr(m)*G(k,m) - Vm(m)*B(k,m)) - Vr(k)*(Vm(m)*G(k,m)+Vr(m)*B(k,m));
    end
    dPQ(k,1)  =  Pesp(k) - PQcalc(k,1);
    dPQ(k+n,1) = Qesp(k) - PQcalc(k+n,1);
    if barras(k,2) == 2
        dPQ(k+n,1) = 0;
        dPQ(k,1) = 0;
    end
    
    if barras(k,2) == 1 % Barra PV
        aux = aux+1;
        dPQ(2*k+aux,1) = V(k)^2-(Vr(k)^2+Vm(k)^2);       
    end
end

% Vetor das vari�veis de estado quando h� barra PV
if find(barras(:,2) == 1)
    VrVm = [VrVm; V(barras_pv)];
end
tic
itera   = 0;
while max(abs(dPQ)) > tolera && itera <=50
    itera = itera + 1;
    
    % Montagem da Jacobiana
    J= zeros(2*n,2*n);
    for m=1:n
        for k=1:n
            if m==k
                J(m,m)=  Vr(m)*G(m,m) + Vm(m)*B(m,m) + Ir(m);     %-->Hkk
                J(m,m+n)= -Vr(m)*B(m,m) + Vm(m)*G(m,m) + Im(m);   %-->Nkk
                J(m+n,m)= -Vr(m)*B(m,m) + Vm(m)*G(m,m) - Im(m);   %-->Mkk
                J(m+n,m+n)= -Vr(m)*G(m,m) - Vm(m)*B(m,m) + Ir(m); %-->Lkk
            else
                J(m,k)=  Vr(m)*G(m,k) + Vm(m)*B(m,k);         %-->Hkm
                J(m,k+n)= -Vr(m)*B(m,k) + Vm(m)*G(m,k);       %-->Nkm
                J(m+n,k)= -Vr(m)*B(m,k) + Vm(m)*G(m,k);       %-->Mkm
                J(m+n,k+n)= -Vr(m)*G(m,k) - Vm(m)*B(m,k);     %-->Lkm
            end
        end
    end
    
    for m=1:n
        if barras(m,2)== 2         %Se Barra do tipo V-Teta
            J(m,m)= 10^10;         %Iguala elemento diagonal da matriz H a infinito
            J(m+n,m+n)= 10^10;     %Iguala elemento diagonal da matriz L a infinito
        end

    end
    
    % Controle de barra PV (Linha e Coluna adicional)
    aux=0;
    for ii=1:n
        if barras(ii,2)==1        %Barra do tipo PV
            aux=aux+1;
            J(2*n+aux,ii) = 2*Vr(ii);  %T
            J(2*n+aux,ii+n) = 2*Vm(ii);%U
            J(n+ii, 2*n+aux) = -1;
            dPQ(2*n+aux,1)= V(ii)^2 - (Vr(ii)^2 + Vm(ii)^2);
        end
    end
    
    dVrVm= J\dPQ;             %[dPQ] = [J].[dOV]
    VrVm  = VrVm + dVrVm;     % Atualiza��o dos resultados
    
    %Atualiza��o das tens�es e pot�ncia reativa gerada na barra PV
    Vr = VrVm(1:n);
    Vm = VrVm((1+n):(2*n));
    
    if numel(find(barras(:,2)==1)) ~= 0
    qger(barras_pv,1) = VrVm(2*n+1:end);
    end
      
    % C�lculo das novas correntes
    I  = Y*(Vr + 1i*Vm);
    Ir = real(I);
    Im = imag(I);
    
    % C�lculo das novas pot�ncias
    Pcalc  = Vr.*Ir + Vm.*Im;
    Qcalc  = Vm.*Ir - Vr.*Im;
        
    % C�lculo dos residuos de pot�ncias   
    aux1 = 0;
    for k=1:n
        dPQ(k,1)  =  Pesp(k) - Pcalc(k,1);
        %            |______Qesp_____|
        dPQ(k+n,1) = (qger(k) - Qd(k)) - Qcalc(k,1);
        
        if barras(k,2) == 2 % Barra VO
            dPQ(k+n,1) = 0;
            dPQ(k,1) = 0;
        end

        if barras(k,2) == 1 % Barra PV
            aux1 = aux1+1;
            dPQ(2*k+aux1,1) = V(k)^2-(Vr(k)^2+Vm(k)^2);            
        end
    end
    %-------------------
    
    if itera >=51
        disp(" N�o convergiu ")
    end
end % Fim fo processo iterativo
t=toc
% Transforma��opara cordenada polar
[O,V]= cart2pol(Vr,Vm);

% C�lculo de P e Q l�quidas para as barras VO e Q para as
for k = 1:n
 
    if barras(k,2) ~= 0
        Q(k) = 0;
        
        if barras(k,2) == 2
            P(k) = 0;
        end
        
        for m = 1:barras_ligadas(k,n+1)
            P(k,1)   = P(k,1) + ...
                Vr(k)*(Vr(m)*G(k,m) - Vm(m)*B(k,m)) + Vm(k)*(Vm(m)*G(k,m)+Vr(m)*B(k,m));
            
            Q(k,1) = Q(k,1) + ...
                Vm(k)*(Vr(m)*G(k,m) - Vm(m)*B(k,m)) - Vr(k)*(Vm(m)*G(k,m)+Vr(m)*B(k,m));            
       end
    end
    
    if barras(k,2) == 2 % Barra VO
        pger(k) = P(k) + Pd(k);
        qger(k) = Q(k) + Qd(k);
    end
end

%-------------------------
% Impress�o dos Resultados
%-------------------------
fprintf(' \n O processo convergiu em %1.0f itera��es  \n\n ',itera);

fprintf('%s\n' ,   '====================================================================================');
fprintf('%s\n'   , '                                      Dados das Barras');
fprintf('%s\n' ,   '====================================================================================');
fprintf('%s\n'   , '+-------+---------------+------------+----------+------------+----------+-----------+');
fprintf('%s\n'   , '| Barra | Tens�o (p.u.) |  Fase (�)  |  Pg(MW)  |  Qg(MVAr)  |  Pd(MW)  |  Qd(MVAr) | ');
fprintf('%s\n'   , '+-------+---------------+------------+----------+------------+----------+-----------+');
for k = 1:n
    fprintf('%s'    ,'| ');
    fprintf('%4.0f' ,barras(k,1));
    fprintf('%s'    ,'  |    ');
    fprintf('%6.3f',V(k));
    fprintf('%s'    ,'     |   ');
    fprintf('%6.2f' ,O(k).*(180/pi));
    fprintf('%s'    ,'   |');
    fprintf('%7.2f',pger(k)*pb);
    fprintf('%s'    ,'   |');
    fprintf('%8.2f',qger(k)*pb);
    fprintf('%s'    ,'    |');
    fprintf('%7.2f',Pd(k)*pb);
    fprintf('%s'    ,'   |');
    fprintf('%7.2f',Qd(k)*pb);
    fprintf('%s\n'  ,'    |');
end
fprintf('%s\n'   , '+-------+---------------+------------+----------+------------+----------+-----------+');