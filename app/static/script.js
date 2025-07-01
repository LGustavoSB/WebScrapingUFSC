
const dados_teste = [{title: 'a', value: 1}, {title: 'b', value: 2}]
let titles = document.createElement('div')
const data_container = document.getElementById('data_container')
dados_teste.forEach(dado => {
    let text = document.createElement('p')
    text.innerText = dado.title
    titles.appendChild(text)
})
data_container.appendChild(titles)