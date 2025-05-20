import IMessage from './messages';


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
  msgId: string;
  userId: string;
  timeCode: Date;
  message: string;
  deleted: boolean;
}
