const express = require('express')
const redis = require('redis')

const client = redis.createClient({ host: process.env.REDIS_HOST || 'localhost' })

client.on('error', console.log)

const app = express()

app.use(express.static('.'))

app.get('/item/:item/user/:user/rating/:rating', (req, res) => {
	let {item, user, rating} = req.params
	item = parseInt(item)
	user = parseInt(user)
	rating = parseInt(rating)

	if (isNaN(item) || isNaN(user) || isNaN(rating)) {
		return res.sendStatus(400)
	}

	client.lpush('qiu', `${item}:${user}:${rating}`, err => {
		return res.status(err ? 400 : 200).json(err ? err : null)
	})
})

app.get('/sim/:name', (req, res) => {
	// const name = req.params.name.toLowerCase()
	// const items = rows.filter(row => row.vacancy.indexOf(name) !== -1)
	// const input = items[Math.floor(Math.random() * items.length)]

	// client.zrange(input.item, 0, -1, 'withscores', (err, data) => {
	// 	let output = []
	// 	for (let i = 0; i < data.length; i += 2) {
	// 		const item = data[i]
	// 		const score = Math.round((-1 * data[i + 1]) * 100) / 100
	// 		output.push({ item, score })
	// 	}
	// 	output = output.map(o => {
	// 		o.vacancy = (rows.filter(r => r.item == o.item).shift() || { vacancy: '' }).vacancy
	// 		return o
	// 	})

	// 	res.json({ input, output })
	// })
})

app.listen(process.env.PORT || 3000)
