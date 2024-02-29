def app():
    import ez

    ez.run()

    return ez._app


if __name__ == "__main__":
    import uvicorn, os
    from args import args, unparsed_args

    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=os.environ.get("ENV", "").lower() == "development",
        log_level="debug",
        factory=True,
        reload_includes=args.reload_include,
    )
