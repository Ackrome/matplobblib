# Описание
Если вы открыли этот модуль библиотеки `matplobblib` и не знаете, что делать, то вот маленькая инструкция:

- `description()` выведет список тем и для каждой темы будет список функций, решающих определенную задачу по теме

- `description([key])`, где  `key` - название темы в формате **str**, выведет список функций с соответсвующими описаниями задач

- `description([key, func])`, где  `key` - название темы в формате **str**, a `func` - название функции в формате **str**, выведет код этой самой функции

Также в данный момент доступно использование всех функций модуля без интеграции кода в ваш проект - иными словами, **вы можете решать задачи так же, подставляя аргументы в функции**, но внутреннюю часть этиъ функций вы видеть не будете. Разве это не замечательно?