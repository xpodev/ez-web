import sys
import os

for path in os.environ["EZ_PYTHONPATH"].split(os.pathsep):
    sys.path.append(path)


def app():
    import ez

    ez.run()

    return ez._app


if __name__ == "__main__":
    import uvicorn
    from args import args, unparsed_args

    uvicorn.run("main:app", host=args.host, port=args.port, reload=True, log_level="debug", factory=True)
