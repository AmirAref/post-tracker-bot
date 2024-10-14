from post_tracker import PostTracker

from src.logger import get_logger


logger = get_logger(__name__)


class PostTrackerWrapper:
    tracker_app: None | PostTracker = None

    def start(self):
        self.tracker_app = PostTracker()
        logger.debug("PostTacker app started !")

    async def stop(self):
        if self.tracker_app is not None:
            await self.tracker_app.close()
            self.tracker_app = None
            logger.debug("PostTacker app stopped!")

    def __call__(self):
        # Ensure we don't use it if not started / running
        assert self.tracker_app is not None
        return self.tracker_app
