if __name__ == "__main__":
    import uvicorn
    from args import args, unparsed_args

    uvicorn.run(
        "core.startup.ez_dev_app:app",
        host=args.host,
        port=args.port,
        reload=True,
        log_level="debug",
        factory=False,
        reload_includes=args.reload_includes,
    )
