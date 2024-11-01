const express = require('express');
const axios = require('axios')

const app = express()

app.all('*', function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    res.header('Access-Control-Allow-Methods', '*');
    res.header('Content-Type', 'application/json;charset=utf-8');
    next();
});

app.get('/weibo', async(req, res) => {
    try {
        let data = await get_data();
        res.send(data);
    } catch (e) {
        res.send('0');
    }
})

async function get_data() {
    let dataList = []
    let { data } = await axios.get('https://weibo.com/ajax/side/hotSearch');
    let data_json = data.data.realtime
    let jyzy = {
        '电影': '影',
        '剧集': '剧',
        '综艺': '综',
        '音乐': '音'
    };

    for (let i = 0; i < data_json.length; i++) {
        let hot = ''
        
        if ('is_ad' in data_json[i] == true) {
            continue;
        } 
        if ('flag_desc' in data_json[i] == true) {
            hot = jyzy[data_json[i]['flag_desc']]
        } 
        if ('is_boom' in data_json[i] == true) {
            hot = '爆'
        }
        if ('is_hot' in data_json[i] == true) {
            hot = '热'
        } 
        if ('is_fei' in data_json[i] == true) {
            hot = '沸'
        } 
        if ('is_new' in data_json[i] == true) {
            hot = '新'
        }
        
        let dic = {
            'title': data_json[i]['note'],
            'url': 'https://s.weibo.com/weibo?q=%23' + data_json[i]['word'] + '%23',
            'num': data_json[i]['num'],
            'hot': hot
        }
        
        dataList.push(dic)
    }
    return dataList
}



app.listen(3000)
