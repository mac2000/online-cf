const express = require('express')
const redis = require('redis')
const cors = require('cors')

const client = redis.createClient({ host: process.env.redis || 'localhost' })

client.on('error', console.log)

const app = express()

app.use(cors())
app.use(express.static('.'))

app.get('/item/:item/user/:user/rating/:rating', (req, res) => {
	let {item, user, rating} = req.params

	if (!item || !user || isNaN(parseInt(rating))) {
		return res.sendStatus(400)
	}

	client.lpush('qiu', `${item}:${user}:${parseInt(rating)}`, err => {
		return res.status(err ? 400 : 200).json(err ? err : 'OK')
	})
})

app.get('/item/:item/related', (req, res) => {
	let {item} = req.params

	client.zrange('s' + item, 0, -1, 'withscores', (err, data) => {
		let output = []

		for (let i = 0; i < data.length; i += 2) {
			const item = data[i]
			const score = Math.round((-1 * data[i + 1]) * 100) / 100
			output.push({ item, score })
		}

		res.json(output)
	})
})

app.listen(process.env.PORT || 3000)
