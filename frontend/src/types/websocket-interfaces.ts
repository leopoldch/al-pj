import IMessage from "./messages";
import IBucketPoint from "./bucketspoints";

export interface MessageViewed {
  msgId: string;
  userId: string;
  timeCode: Date;
}

export interface MessageCreated {
  message: IMessage;
  sender: {
    id: number;
    email: string;
    username: string;
  };
}

export interface MessageDeleted {
  message: IMessage;
  sender: {
    id: number;
    email: string;
    username: string;
  };
}

export interface Presence {
  user_id: number;
  name: string;
}

export interface BucketPointDeleted {
  id: number;
}

export interface BucketPointCreated {
  data: IBucketPoint;
}

export interface BucketPointUpdated {
  data: IBucketPoint;
}
