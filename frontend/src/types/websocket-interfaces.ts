import IMessage from "./messages";

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
