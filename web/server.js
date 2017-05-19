const express = require('express')
const fs = require('fs')
const parse = require('csv-parse/lib/sync')
const redis = require('redis')

const client = redis.createClient({ host: 'r3' })

client.on('error', console.log)

const rows = parse(fs.readFileSync('vacancies.csv', 'utf-8'), { columns: true }).map(r => {
	r.vacancy = r.vacancy.trim().toLowerCase()
	return r
})

const app = express()

app.use(express.static('.'))

app.get('/sim/:name', (req, res) => {
	const name = req.params.name.toLowerCase()
	const items = rows.filter(row => row.vacancy.indexOf(name) !== -1)
	const input = items[Math.floor(Math.random() * items.length)]

	client.zrange(input.item, 0, -1, 'withscores', (err, data) => {
		let output = []
		for (let i = 0; i < data.length; i += 2) {
			const item = data[i]
			const score = Math.round((-1 * data[i + 1]) * 100) / 100
			output.push({ item, score })
		}
		output = output.map(o => {
			o.vacancy = (rows.filter(r => r.item == o.item).shift() || { vacancy: '' }).vacancy
			return o
		})

		res.json({ input, output })
	})
})

app.listen(process.env.PORT || 3000)
