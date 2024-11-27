# Modelo de dados dos objetos em Python

O modelo de objetos em python é baseado, em boa medida, na existência e implementação de métodos especiais (métodos *dunder*/speciais) que permitem que os mesmos objetos sejam trabalhados de forma consistente e intuitiva por meio da API padrão da própria linguagem.
Tais métodos especiais garantem que uma mesma API própria da linguagem (`len`, `sum`, `for ... in ... :`, `x[i]`, por exemplo) possa também operar em cima de classes(e tipos) quaisquer definidos pelo usuário.

A implementação destes métodos especiais ocorre quando há a necessidade de que objetos definidos suportem e interajam com elementos fundamentais da linguagem, tais como:
- Coleções
- Acesso a atributos
- Iteração
- Sobrecarga de operadores
- Invocação de funções e métodos
- Representação e formatação de strings
- Programação assíncrona
- Criação e destruição de objetos
- Contextos gerenciados, por meio das instruções `with` ou `async with`.

## Exemplo de implementação de um baralho pythônico

Deseja-se construir uma classe que represente um baralho de cartas.
Ao implementar determinados métodos especiais, é então possível fazer uso desta classe como se fosse um sequência.
Inclusive fazendo-se uso da API nativa da linguagem para tal.

```python
import collections

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
````

Por meio da implementação de `__len__` e `__getitem__` e fazendo uso do modelo de dados, é possível fazer uso de uma série de operações da API nativa da linguagem, tais como:
- Cálculo da quantidade de itens
- Acesso de determinada carta pela sua posição
- Acesso de fatias de cartas da coleção
- Realizar operações arbitrárias de ordenamento do deck
Demais exemplos demonstrativos estão contidos no arquivo `codigo.py`, função `exemplo_1()`.

Importante observar que não é necessário herdar de nenhuma outra classe para se ter esse comportamento.
Bastando apenas a implementação dos métodos especiais em específico para que a API nativa possa realizar suas operações.
Dá-se o nome de *duck typing* para este tipo de estratégia e mecanismo.

## Emulando tipos numéricos

Implementa-se agora outro exemplo para elucidar o uso dos métodos especiais.
Trata-se da construção de uma classe que represente um vetor no espaço euclidiano e consequentemente a implementação de operações básicas de soma entre esses tipos.

```python
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self, other):
        return bool(abs(self))

    def __add__(self, other: Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
```

Os exemplos de utilização estão mostrados no `exemplo_2()` do arquivo `codigo.py`.
É possível perceber que apenas o interpredor Python faz uso dos métodos especiais para realização das operações.
Desta forma faz-se uso de todo o arcabouço que a linguagem já traz nativamente.
Importante também notar que os métodos `__add__` e `__mul__` retornam novos objetos e não realização mutação local dos atributos da instância, e este comportamente é dado por convenção.
Caso seja necessário operações de mutação *in-place* da instância, deve-se fazer uso dos métodos `__iadd__`, `__imul__` e quaisquer outros métodos da respectiva família `__i*__`.
O método `__repr__`, que é utilizado pela função `repr` embutida, serve para se obter a representação do objeto, como string, para inspeção.
Tanto o console iterativo quanto o depurador fazem uso do `repr` para exibir o resultado das expressões.
A string devolvida por `__repr__` deve não ser ambígua e, se possível, deve corresponder ao código-fonte necessário para recriar o objeto representado.
Já por outro lado, a string retornada por `__str__` é mais adequada para exibição ao usuário, com esta podendo ter seu resultado final mais customizável.

## A API de _collections_

A Figura 1 mostra o diagrama UML do modelo de dados em python para `collections.abc`, com informações adicionais de [docs.python.org/reference/datamodel](https://docs.python.org/3.13/reference/datamodel.html) e [docs.python.org/library/collections.abc](https://docs.python.org/3.13/library/collections.abc.html#module-collections.abc).
As classes representadas no diagrama são classes base abstratas (*ABCs*), advindas do módulo `collections.abc`.

| *Figura 1 - Diagrama UML do modelo de dados em python (_collections.abc_)* |
|:--:|
| ![Diagrama UML do modelo de dados em python](./diagrama_UML_modelo_dados_python.svg) |

Tais *ABCs* definem interfaces abstratas que precisam ser implementadas para que determinada classe qualquer possa ser tratada como cada uma das categorias ali representadas.
Os nomes em itálico são métodos abstratos, enquanto que os nomes em fonte normal são métodos _mixin_.
Cada uma das classes ali dão suporte a comportamentos e APIs específicas, tais como:
- `Iterable`: `for ... in ... :`, desempacotamento e outras formas de iteração;
- `Sized`: função embutida `len`;
- `Container`: operador `in`;

Graças à estratégia de *duck typing*, as classes concretas não precisam necessariamente herdar das *ABCs*, bastando apenas realizar a implementação dos respectivos métodos especiais.

Ainda sobre as classes do grupo `Collection`:
- `Sequence` formaliza a interface de tipos embutidos como `list` e `str`;
- `Mapping` representa a interface de tipos como `dict`, `collections.defaultdict`, etc;
- `Set` representa a interface dos tipos embutidos `set`e `frozenset`.

## Visão geral dos métodos especiais

Na Tabela 1 estão reunidos os nomes dos métodos especias e suas respectivas categorias, excluindo os métodos utilizados para operadores infixos e funções matemáticas fundamentais.

<table style="margin: 0px auto;">
  <tr style="text-align: center; font-style: italic; font-weight: bold;"><td colspan="2">Tabela 1 - Nomes dos métodos especias e respectivas categorias</td></tr>
  <tr style="text-align: center;"><th>Categoria</th> <th>Nomes dos métodos</th></tr>
  <tr><td>Representação de string/bytes</td> <td>__repr__ __str__ __format__ __bytes__ __fspath__</td></tr>
  <tr><td>Conversão para número</td> <td>__bool__ __complex__ __int__ __float__ __hash__ __index__</td></tr>
  <tr><td>Emulação de coleções</td> <td>__len__ __getitem__ __setitem__ __delitem__ __contains__</td></tr>
  <tr><td>Iteração</td> <td>__iter__ __aiter__ __next__ __anext__ __reversed__</td></tr>
  <tr><td>Execução de chamável ou corrotina</td> <td>__call__ __await__</td></tr>
  <tr><td>Gerenciamento de contexto</td> <td>__enter__ __exit__ __aenter__ __aexit__</td></tr>
  <tr><td>Criação e destruição de instâncias</td> <td>__new__ __init__ __del__</td></tr>
  <tr><td>Gerenciamento de atributos</td> <td>__getattr__ __getattribute__ __setattr__ __delattr__ __dir__</td></tr>
  <tr><td>Descritores de atributos</td> <td>__get__ __set__ __delete__ __set_name__</td></tr>
  <tr><td>Classes base abstratas</td> <td>__instancecheck__ __subclasscheck__</td></tr>
  <tr><td>Metaprogramação de classes</td> <td>__prepare__ __init_subclass__ __class_getitem__ __mro_entries__</td></tr>
</table>

<br/>
Adicionalmente, estão listados na Tabela 2 os operadores infixos e numéricos suportados pelos métodos especiais.
<br/>
<br/>

<table style="margin: 0px auto;">
  <tr style="text-align: center; font-style: italic; font-weight: bold;"><td colspan="3">Tabela 2 - Nomes e símbolos de métodos especiais para operadores</td></tr>
  <tr style="text-align: center;"><th>Categoria do operador</th> <th>Símbolos</th> <th>Nomes dos métodos</th></tr>
  <tr><td>Unário numérico</td> <td>- + abs()</td> <td>__neg__ __pos__ __pos__</td></tr>
  <tr><td>Comparação rica</td> <td>< <= == != > >=</td> <td>__lt__ __le__ __eq__ __ne__ __gt__ __ge__</td></tr>
  <tr><td>Aritmético</td> <td>+ - * / // % @ divmod() round() ** pow()</td> <td>__add__ __sub__ __mul__ __truediv__ __floordiv__ __mod__ __matmul__ __divmod__ __round__ __pow__</td></tr>
  <tr><td>Aritmética reversa</td> <td>Todos os operadores aritméticos com os operandos invertidos</td> <td>__radd__ __rsub__ __rmul__ __rtruediv__ __rfloordiv__ __rmod__ __rmatmul__ __rdivmod__ __rpow__</td></tr>
  <tr><td>Atribuição aritmética aumentada</td> <td>+= -= *= /= //= %= @= **=</td> <td>__iadd__ __isub__ __imul__ __itruediv__ __ifloordiv__ __imod__ __imatmul__ __ipow__</td></tr>
  <tr><td>Bit a bit</td> <td>& | ^ <<<p hidden><</p> >> ~</td> <td>__and__ __or__ __xor__ __lshift__ __rshift__ __invert__</td></tr>
  <tr><td>Bit a bit reversa</td> <td>Todos os operadores bit a bit com os operandos invertidos</td> <td>__rand__ __ror__ __rxor__ __rlshift__ __rrshift__</td></tr>
  <tr><td>Atribuição bit a bit aumentada</td> <td>&= |= ^= <<<p hidden><</p>= >>=</td> <td>__iand__ __ior__ __ixor__ __ilshift__ __irshift__</td></tr>
</table>

## Considerações adicionais sobre o modelo de dados

Seguem adiante mais considerações de interesse obtidas da documentação oficial [docs.python.org/reference/datamodel](https://docs.python.org/3.13/reference/datamodel.html).

#### Nomes dos métodos especiais

São apresentados nesta seção os nomes dos métodos especiais que são invocados pela API nativa, organizados em categorias específicas.
Esta é a abordagem para sobrecarga de operadores em Python, permitindo que as próprias classes definam seu próprio comportamento diante dos operadores da linguagem.
Exceto em casos específicos, tentativas de executar uma operação devem acusar uma _exceção_ quando não há método apropriado definido (tipicamente `AttributeError` ou `TypeError`).
Retornando `None` de um método especial indica que este não está disponível para a respectiva operação.

_Customização básica_:
- `__new__(cls[,...])`:
Invocado no momento de criação de uma nova instância de uma classe.
Trata-se de um método estático que recebe a classe como primeiro argumento.
Argumentos restantes são repassados para o construtor do objeto.
O valor de retorno deve ser uma nova instância (geralmente uma nova instância de _cls_).
De forma geral, cria-se a nova instância invocando o método `__new__()` da superclasse por meio de `super().__new__(cls[,..])` e então modificando a nova instância da forma que for necessário antes de retorná-la.
Se `__new__()` retornar uma nova instância de _cls_, então o método `__init__()` desta será invocado como `__init__(self[,...])`, em que _self_ é a nova instância e os argumentos restantes são os mesmos informados pelo construtor do objeto.
Se `__new__()` não retornar uma nova instância de _cls_, então o método `__init__()` não será invocado;
- `__init__(self[,...])`:
Invocado após a instância ser criada pelo método `__new__()`, mas antes desta ser retornada para o invocador.
Os argumentos são os mesmos passados para o construtor.
Se a classe base possui um método `__init__()`, a subclasse, se também o possuir, deve explícitamente invocá-lo para garatir a correta inicialização da instância, como por exemplo `super().__init__([args...])`;
- `__del__(self)`:
Invocado quando a instância está para ser destruída.
Se a classe base possui um método `__del__()`, a subclasse, se também o possuir, deve explícitamente invocá-lo para garatir a correta destruição da instância.
Não há garantia de que o método `__del__()` seja invocado nos objetos que ainda persistem com a finalização do interpretador.
`weakref.finalize` provém uma forma direta de registrar uma função de limpeza a ser invocada quando o objeto é removido pelo _garbage collector_;
;
- `__repr__(self)`:
Invocado pela função embutida `repr()` para criar a representação de string "oficial" do objeto.
Tanto quanto possível, esta representação deve ser uma expressão Python válida que pode ser usada para a recriação do objeto com o mesmo valor (para um mesmo ambiente).
Se não for possível, uma string no formato `<...alguma descrição útil...>` deve ser retornada.
O valor a ser retornado deve ser do tipo `string`.
Se uma classe define `__repr__()`, mas não `__str__()`, então `__repr__()` é também utilizado para a criar a representação de string "informal" quando necessário.
Este método é normalmente utilizado para depuração e portanto é interessante que sua representação seja rica em detalhes e não ambígua.
A umplementação padrão é provida pela própria classe `object`;
- `__str__(self)`:
Invocado pela função `str(object)`, a implementação `__format__()` padrão, e pela função embutida `print()` para criar a representação "informal" de string da instância.
O valor de retorno deve ser uma string.
Difere de `__repr__()` na forma de que não há a expectativa de que a representação seja uma expressão Python válida.
Podendo então ser uma representação mais concisa e conveniente.
A implementação padrão é definida pelo tipo `object` por meio do método `__repr__()`;
- `__bytes__(self)`:
Invocado por `bytes` para retornar a representação de byte-string de um objeto.
Deve retornar um objeto do tipo `bytes`.
A classe `object` não provém estem método por padrão;
- `__format__(self, format_spec)`:
Invocado pela função embutida `format()`, e por extensão, pelo método `str.format()` e avaliação de strings literais formatadas para criar uma representação "formatada" de string do objeto.
O argumento _format_spec_ é uma string que descreve as opções de formatação desejadas.
A interpretação do argumento _format_spec_ é responsabilidade do tipo que está implementando `__format__()`.
Entretanto, a maioria das classes terminam por delegar a implementação para um dos tipos embutidos ou empregar sintaxe similar de formatação.
Ver [Format Specification Mini-Language](https://docs.python.org/3.13/library/string.html#formatspec) para descrição da sintaxe de formatação padrão.
O valor de retorno deve ser uma string.
A implementação padrão pela classe `object`deve ser dada com o argumento _format_spec_ vazio, delegando para o método `__str__()`;
- `__lt__(self, other)` <br/>
`__le__(self, other)` <br/>
`__eq__(self, other)` <br/>
`__ne__(self, other)` <br/>
`__gt__(self, other)` <br/>
`__ge__(self, other)`:
Estes métodos também são chamados de métodos de "comparação rica".
A correspondência entre símbolos de operadores e nomes dos métodos segue: `x<y` invoca `x.__lt__(y)`, `x<=y` invoca `x.__le__(y)`, `x==y` invoca `x.__eq__(y)`, `x!=y` invoca `x.__ne__(y)`, `x>y` invoca `x.__gt__(y)` e `x>=y` invoca `x.__ge__(y)`.
Qualquer um destes métodos pode restornar `NotImplemented` se a classe não implementar o respectivo método para o seu correspondente operador.
Por convenção `False` ou `True`são retornados após uma comparação bem sucedida.
Entretanto, tais métodos podem retornar quaisquer valores, e se este método for empregado num contexto de avaliação Booleana, Python invocará `bool()` sobre o valor retornado para determinar se o resultado é `True`ou `False`.
Por padrão, `object` implementa `__eq__()` utilizando `is` e retornando `NotImplemented` caso a comparação resulte falsa.
Para `__ne__()`, por padrão é delegada para `__eq__()` e seu resultado é invertido, caso não resulte em `NotImplemented`.
Não há mais outras relações implícitas entre quaisquer outros operadores.
Por exemplo, a verdade de `(x<y or x==y)` não implica que `x<=y`.
Para realizar a criação automática de operações de ordenamento à partir de uma operação raiz, ver [functools.total_ordering()](https://docs.python.org/3.13/library/functools.html#functools.total_ordering).
Por padrão a classe `object` provém implementação consistente com comparação de valor: equalidade compara de acordo com a identidade do objeto e comparações de ordem levantam `TypeError`.
Cada método padrão pode gerar estes resultados diretamente, mas também podem retornar `NotImplemented`.
Não existem versões com os argumentos trocados destes métodos, já que `__lt__()` e `__gt__()` são reflexo um do outro, assim como também `__le__()` com `__ge__()` e `__eq__()` com `__ne__()`.
Se os operandos forem de tipos diferentes, e o operando da direita for uma subclasse direta ou indireta do operando da esquerda, então o método reflexo do operando da direita possui prioridade, do contrário o método do operando da esquerda possuirá prioridade.
Quando nenhum método apropriado retornar nenhum outro valor além de `NotImplemented`, os operadores `==` e `!=` retornam para os operadores `is` e `is not`, repectivamente;
- `__hash__(self)`:
Invocado pela função embutida `hash()` e por operações em instâncias de coleções hasheadas incluindo `set`, `frozenset` e `dict`.
Deve retornar valor do tipo inteiro.
A única propriedade requerida é que objetos que devem resultar equivalentes, devem possuir o mesmo valor hash.
Recomenda-se incluir na construção do valor hash os componentes constinuintes do objeto que sejam de interesse para a operação de comparação.
Por exemplo, pode-se incluí-los numa tupla e retornando o valor hash da tupla resultante.
Se uma classe não definir o método `__eq__()`, esta também não deve definir o método `__hash__()`.
Se a classe define o método `__eq__()`, mas não define o método `__hash__()`, suas instâncias não poderão ser utilizadas como itens em coleções hasheadas.
Se a classe define objetos mutáveis e implementa o método `__eq__()`, então esta não deve implementar `__hash__()`, dado o fato que a implementação de coleções hasheadas requer que o valor hash da chave seja imutável.
Classes definidas pelo usuário possuem os métodos `__eq__()` e `__hash__()` por padrão, herdados da classe `object`, e desta forma seus objetos resultarão não equivalentes a menos que comparados consigo mesmos e `x.__hash__()` retornará valor tal que `x == y` implica que ambos `x is y` e `hash(x) == hash(y)`.
Uma classe que sobrescreve `__eq__()`e não define `__hash__()` terá seu método `__hash__()` retornando o valor `None` de forma implícita, levantando o erro `TypeError` quando houver tentativa de se obter seu valor hash, além de também ser identificada como classe não hasheável ao realizar a verificação `isinstance(obj, collection.abc.Hashable)`.
Se uma classe que sobrescreve `__eq__()` precisar reter a implementação `__hash__()` de uma classe superior, deve-se deixar isso de forma explícita por meio de `__hash__ = <ParentClass>.__hash__`.
Se uma classe não sobrescreve `__eq__()` e desejar suprimir o suporte à funçao de hash, então deve-se incluir na definição da classe `__hash__ = None`.
Uma classe que possui sua própria definição de `__hash__()` que explicitamente levanta o erro `TypeError` seria incorretamente identificada como hasheável pela chamada `isinstance(obj, collections.abc.Hashable)`;
- `__bool__(self)`:
Invocado para implementação de testes de verdade da função embutida `bool()`.
Deve retornar `False` ou `True`.
Quando este método não é definido, o método `__len__()` é chamado e o objeto é considerado `True` se o resultado for não zero.
Se a classe não implementar nem `__bool__()` e `__len__()` (que é o caso da classe `object`), então todas suas instâncias são consideradas `True`;

_Customização de acesso dos atributos de instâncias de classes_:
- `__getattr__(self, name)`:
Invocado quando o acesso padrão ao atributo falha com o erro `AttributeError` (seja porque o método `__getattribute__()` acusou `AttributeError` pelo _nome_ não ser um atributo de instância ou atributo de classe para `self`, ou pela chamada de `__get__()` de uma propriedade _nome_ ter acusado `AttributeError`).
Deve retornar o valor do atributo computado ou acusar `AttributeError`.
A classe `object` não provém este método.
Se o atributo for encontrado por meio do mecanismo convencional, este método não será chamado;
- `__getattribute__(self, name)`:
Invocado incondicionalmente para implementar acessos de atributos de instâncias e classes.
Se a classe também implementar `__getattr__()`, a mesma não será chamada, a menos que `__getattribute__()` chame explícitamente, ou acuse `AttributeError`.
Este método deve retornar o valor computado do atributo ou acusar `AttributeError`.
Para evitar recursão infinita, sua implementação deve sempre chamar o método da classe superior com o mesmo _nome_ para acessar qualquer atributo necessário, como por exemplo `object.__getattribute__(self, name)`.
Para certos acessos sensíveis de atributos, também invoca um _evento de auditoria_ `object.__getattr__(obj, name)`;
- `__setattr__(self, name, value)`:
Invocado na tentativa de atribuição de um atributo.
Este método é chamado ao invés do mecanismo convencional (ou seja, guardar o valor no dicionário da instância).
_name_ é o nome do atributo e _value_ é o valor a ser atribuído ao mesmo.
Se `__setattr__()` for usado para atribuição de um atributo de instância, este deve chamar o método correspondente da classe superior, por exemplo `object.__setattr__(self, name, value)`.
Para determinadas atribuições de atributos sensíveis, acusa um _evento de autitoria_ `object.__setattr__(obj, name, value)`;
- `__delattr__(self, name)`:
Similar à `__setattr__()`, mas para operação de deletar um atributo.
Deve ser implementado apenas se `del obj.name` fizer sentido para o objeto.
Para determinadas operações de delete de atributos sensíveis, acusa um _evento de autitoria_ `object.__delattr__(obj, name)`;
- `__dir__(self)`:
Invocado quando a função `dir()` é chamada sobre o objeto.
Deve retornar um iterável.
`dir()` converte o iterável retornado em uma lista e a ordena;

_Customização de acesso de atributos de módulos_:
- `__getattr__(self, name)`:
Deve retornar o valor do atributo ou acusar `AttributeError`.
Se um atributo não for encontrado por meio do mecanismo convencional, por meio de `__getattribute__()` por exemplo, então `__getattr__` é procurado dentro do dicionário `__dict__` do módulo antes de acusar `AttributeError`;
- `__dir__(self)`:
Deve retornar um iterável de strings que representam os nomes acessíveis no módulo.
Se implementado, este método sobrescreve o método `dir()` padrão de busca para o módulo;
- `__class__`:
É possível redefinir este atributo para um módulo para se obter um controle mais refinado sobre o comportamento do mesmo.
Deve-se atribuir este atributo para um objeto do tipo `types.ModuleType`;

_Implementação de descritores_:
- `__get__(self, instance, owner=None)`:
Invocado para obter um atributo da classe portadora ou uma instância daquela classe.
O argumento _owner_ é referente a classe portadora, enquanto que o argumento _instance_ trata da instância da mesma classe.
Deve retornar o atributo computado ou acusar `AttributeError`;
- `__set__(self, instance, value)`:
Chamado para realizar a atribuição de um atributo em uma instância _instance_ da classe portadora, com um novo valor _value_.
Realizando-se a implementação de `__set__()` ou `__delete__()` faz o descritor ser do tipo _data descriptor_;
- `__delete__(self, instance)`:
Invocado para deletar um atributo de uma instância _instance_ da classe portadora;

_Customização da criação de classes_:
- `__init_subclass__(cls)`:
Invocado na classe superior toda vez que uma classe herda de outra classe.
Desta forma é possível escrever classes que alteram o comportamento de suas subclasses, de modo similar à um decorador de classes.
Entretanto, enquanto um decorador de classes altera apenas a classe específica em que ele é aplicado, este método age sobre as futuras subclasses da classe superior que o implementa.
O argumento _clas_ é referente à nova subclasse.
Se definido como um método de instância convencional, é implicitamente convertodo para método de classe.
Argumentos chave (_keyword_) dados para a nova classe são passados por meio do método `__init_subclass__()` da classe superior.
A implementação padrão não faz nada, mas acusa erro se chamada com qualquer um argumento.
A dica `metaclass` é consumida pelo sistema de tipos e nunca é repassada para a implementação de `__init_subclass__()`;
- `__set_name__(self, owner, name)`:
Invocado automaticamente no momento que a classe portadora _owner_ é criada;
- `__mro_entries__(self, bases)`:
Se uma base que está presente na definição de uma classe não for uma instância de `type`, então um método `__mro_entries__()` é buscado nesta base.
Case seja encontrado, então a base é substituída com o resultado da chamada de `__mro_entries__()` no momento de criação da classe.
O método é invocado com uma tupla das bases originais como argumento _bases_ e retorna uma tupla de classes que serão utilizadas em seu lugar.
O método pode restornar uma tupla vazio, e neste caso, a base original é ignorada;

_Customização das verificações de instância e subclasse_:

Estes métodos servem para sobrescrever os comportamentos padrões das funções embutidas `isinstance()` e `issubclass()`.

- `__instancecheck__(self, instance)`:
Deve retornar `True`se uma instância _instance_ for considerada (direta ou indiretamente) uma instância da classe;
- `__subclasscheck__(self, subclass)`:
Deve retornar `True`se uma subclasse _subclass_ for considerada (direta ou indiretamente) uma subclasse da classe;

_Emulando objetos chamáveis_:
- `__call__(self[, args...])`:
Chamado quando uma instância é "invocada" como uma função.
A classe `object`não provém este método por padrão;

_Emulando tipos contêiners_:
- `__len__(self)`:
Chamado para implementar a função embutida `len()`.
Deve retornar o comprimento do objeto, um valor inteiro >= 0.
Adicionalmente, um objeto que não tenha definido seu método `__bool__()` ao mesmo tempo que seu método `__len__()` retorne zero será considerado como `False` num contexto booleano;
- `__lengh_hint__(self)`:
Invocado para implementar o operador `.lengh_hint()`.
Deve retornar o valor __estimado__ de comprimento para o objeto (que pode ser maior ou menor que o valor real).
O valor de retorno deve ser um valor inteiro >= 0, ou acusar `NotImplemented`;
- `__getitem__(self, key)`:
Invocado para implementar o operador `self[key]`.
Para tipo de sequência a chave _key_ deve ser um número inteiro.
Pode opcionalmente suportar objetos do tipo _fatia_ e/ou números negativos para o index (chave).
Se _key_ não for do tipo apropriado, deve acusar `TypeError`.
Se _key_ for um valor fora do set de índices para a sequẽncia, deve acusar `IndexError`.
Para tipo de mapeamento, se a chave _key_ não estiver no contêiner e estiver faltando, deve acusar `KeyError`.
Loops para-faça `for` esperam que o erro `IndexError` seja acusado para a interrupção do mecanismo de loop;
- `__setitem__(self, key, value)`:
Chamado para implementar o operador de atribuição para `self[key]`.
Considerações similares à `__getitem__()`.
Deve se apenas implementado para mapeamentos se os objetos suportarem alterações nos valores para as respectivas chaves _key_, ou se novas chaves podem ser adicionadas, ou para sequências em que seus elementos podem ser substituídos.
Os mesmos erros do método `__getitem__()` devem ser acusados para valores impróprios de chave _key_;
- `__delitem__(self, key)`:
Invocado para implementar a operação de deletar para `self[key]`.
Considerações similares à `__getitem__()`.
Deve se apenas implementado para mapeamentos se os objetos suportarem a remoção das respectivas chaves _key_, ou para sequências em que seus elementos podem ser removidos.
Os mesmos erros do método `__getitem__()` devem ser acusados para valores impróprios de chave _key_;
- `__missing__(self, key)`:
Chamado por `dict.__getitem__()` para implementar `self[key]` para subclasses de `dict` quando uma chave _key_ não for encontrada neste dicionário;
- `__iter__(self)`:
Este método é chamado quando um iterador é requisitado para um contêiner qualquer.
Deve retornar um novo objetor iterador que possua capacidade de iterar sobre todos os objetos do contêiner.
Para mapeamentos, este deve iterar sobre as chaves _key_ do contêiner;
- `__reversed__(self)`:
Invocado pela função embutida `reversed()` para implementar a iteração reversa.
Deve retornar um novo objetor iterador que possua capacidade de iterar sobre todos os objetos do contêiner em orderm inversa.
Se este método não for implementado, a função embutida `reversed()` irá fazer uso do protocolo de sequência (`__len__()` e `__getitem__()`).
Os operadores `in` e `not in` são normalmente implementados como uma iteração ao longo de todo o contêiner;
- `__contains__(self, item)`:
Chamado para implementação dos operadores `in` e `not in`.
Devem retornar `True` se o item estiver presentem em `self` e `False` do contrário.
Para objetos do tipo de mapeamento, este deve considerar as chaves _key_ do mapeamento ao invés dos respectivos valores ou pares chave-valor.
Para objetos que não possuem a implementação de `__contains__()`, os testes `in` e `not in` fazem uso dos métodos `__iter__()` e posteriormente `__getitem__()`;

_Emulando tipos numéricos:
- `__add__(self, other)` <br/>
`__sub__(self, other)` <br/>
`__mul__(self, other)` <br/>
`__matmul__(self, other)` <br/>
`__truediv__(self, other)` <br/>
`__floordiv__(self, other)` <br/>
`__mod__(self, other)` <br/>
`__divmod__(self, other)` <br/>
`__pow__(self, other[, modulo])` <br/>
`__lshift__(self, other)` <br/>
`__rshift__(self, other)` <br/>
`__and__(self, other)` <br/>
`__xor__(self, other)` <br/>
`__or__(self, other)`:
Implementam os operadores de operações aritméticas binárias (`+`, `-`, `*`, `@`, `/`, `//`, `%`, `divmod()`, `pow()`, `**`, `<<`, `>>`, `&`, `^` e `|`), respectivamente.
Por exemplo, a expressão `x + y` passa a ser realizada pela chamada de `type(x).__add__(x, y)`.
O método `divmod()` é o equivalente a utilizar o método `__floordiv__()` e `__mod__()`, não devendo ser relacionado com `__truediv__()`.
Se quaisquer um desses métodos não suportarem a operação com os argumentos informados, deve-se retornar com o erro `NotImplemented`;

- `__radd__(self, other)` <br/>
`__rsub__(self, other)` <br/>
`__rmul__(self, other)` <br/>
`__rmatmul__(self, other)` <br/>
`__rtruediv__(self, other)` <br/>
`__rfloordiv__(self, other)` <br/>
`__rmod__(self, other)` <br/>
`__rdivmod__(self, other)` <br/>
`__rpow__(self, other[, modulo])` <br/>
`__rlshift__(self, other)` <br/>
`__rrshift__(self, other)` <br/>
`__rand__(self, other)` <br/>
`__rxor__(self, other)` <br/>
`__ror__(self, other)`:
Estes métodos são chamados para implementar as operações aritméticas binárias com os operandos refletidos (trocados).
São apenas invocados quando o operando da esquerda não suportar a operação correspondente (acusar `NotImplemented`) e/ou quando os operandos são de tipos diferentes.
Se o operando da direita for de uma subclasse do operando da esquerda e esta subclasse prover uma implementação diferente do método de operação refletida, então este método será chamado antes do método não-refletido do operando da esquerda (possui precedência).
Tal comportamento permite que uma subclasse efetue a subrescrita do método da classe superior;

- `__iadd__(self, other)` <br/>
`__isub__(self, other)` <br/>
`__imul__(self, other)` <br/>
`__imatmul__(self, other)` <br/>
`__itruediv__(self, other)` <br/>
`__ifloordiv__(self, other)` <br/>
`__imod__(self, other)` <br/>
`__ipow__(self, other[, modulo])` <br/>
`__ilshift__(self, other)` <br/>
`__irshift__(self, other)` <br/>
`__iand__(self, other)` <br/>
`__ixor__(self, other)` <br/>
`__ior__(self, other)`:
Implementam os operadores de atribuição aritméticas aumentada (`+=`, `-=`, `*=`, `@=`, `/=`, `//=`, `%=`, `**=`, `<<=`, `>>=`, `&=`, `^=` e `|=`), respectivamente.
Estes métodos devem tentar realizar a operação de forma _in-place_, modificando o objeto `self` e retornando o resultado (que pode ser, mas não necessariamente precisa, o próprio objeto `self`).
Se quaisquer um desses métodos não forem definidos ou se acusar a exceção `NotImplemented`, então o método recairá para a sua implementação convencional;

- `__neg__(self)` <br/>
`__pos__(self)` <br/>
`__abs__(self)` <br/>
`__invert__(self)`:
Invocado para a implementação das operação aritméticas unárias (`-`, `+`, `abs()` e `~`);

- `__complex__(self)` <br/>
`__int__(self)` <br/>
`__float__(self)`:
Invocado para a implementação das funções embutidas `complex()`, `int()` e `float()`.
Deve retornar o valor do tipo apropriado;

- `__index__(self)`:
Chamado para implementar o operador `.index()` e quando Python precisa realizar conversão sem perdas de informação de objeto de tipo numérico para inteiro (tal qual fatiamento, ou nas funções embutidas `bin()`, `hex()` e `hex()`).
A presença deste método sugere que o objeto seja do tipo inteiro.
Se os métodos `complex()`, `int()` e `float()` não forem definidos, então as correspondentes funções embutidas recaem para o método `__index__()`;

- `__round__(self[, ndigits])` <br/>
`__trunc__(self)` <br/>
`__floor__(self)` <br/>
`__ceil__(self)`:
Invocado para a implementação das funções embutidas `round()`, `trunc()`, `floor()` e `ceil()`.
A menos que _ndigits_ seja informado para `__round__()`, então todos estes métodos devem retornar o valor truncado para um `Integral`.
A função embutida `int()` recai para `__trunc__()` caso nem `__int__()` ou `__index__()` tenham sido definidas;

_Gerenciadoes de contexto da sintaxe `with`_:
- `__enter__(self)`:
Responsável pela entrada do contexto em tempo de execução para o objeto.
A sintaxe `with` irá atribuir o valor de retorno deste método para o alvo especificado na cláusula `as`, se existir;
- `__exit__(self, exc_type, exc_value, traceback)`:
Responsável pela saída do contexto em tempo de execução para o objeto.
Os parâmetros descrevem a exceção que resultou na saída do contexto de execução.
Se o contexto saiu sem uma exceção, então todos os três argumentos possuirão o valor `None`.
Se uma exceção for alimentada ao método e se deseja suprimí-la (prevenir que a exceção seja propagada), então o seu valor deverá ser `True`.
Do contrário, a exceção será processada normalmente a partir da saída deste método.
Este método não deverá reacusar a exceção passada, pois esta é responsabilidade de que chamou este método;
