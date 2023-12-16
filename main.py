import data_app
import web_app


def main(name:str = __name__) -> int:
	data = data_app.main(10, 10)
	return web_app.main(name, df=data)


if __name__ == '__main__':
	raise SystemExit(main('main'))
