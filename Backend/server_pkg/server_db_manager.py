import sqlite3
import os
import time


class DB_Manager:
    def __init__(self):
        self.conn = sqlite3.connect(
            (str(os.path.dirname(os.path.abspath(__file__)))+'/UserData.db'))

    # record table creation
    def TableCreation(self):
        self.conn.execute('''CREATE TABLE CAMPAIGN  
                        (CID        INTEGER     PRIMARY KEY     AUTOINCREMENT,
                        SID         INTEGER     NOT NULL,
                        Title       TEXT        NOT NULL,
                        Description TEXT        NOT NULL,
                        SDate       INTEGER     NOT NULL,
                        EDate       INTEGER     NOT NULL,
                        Budget      INTEGER     NOT NULL,
                        visibility  TEXT        NOT NULL,
                        goal        TEXT        NOT NULL,
                        flagged     TEXT        NOT NULL);''')
        print("CAMPAIGN Record table created successfully")

        self.conn.execute('''CREATE TABLE AD_REQUEST
                        (AID            INTEGER     PRIMARY KEY     AUTOINCREMENT,
                        CID             INTEGER     NOT NULL,
                        SID             INTEGER     NOT NULL,
                        IID             INTEGER     NOT NULL,
                        REQUEST_FROM    TEXT        NOT NULL,
                        STATUS          TEXT        NOT NULL,
                        TIMESTAMP       INTEGER     NOT NULL,
                        MSG             TEXT        NOT NULL,
                        Budget_nig      TEXT        NOT NULL,
                        TERMS_nig       TEXT        NOT NULL,
                        SEEN_SOPN       TEXT        NOT NULL,
                        SEEN_INFL       TEXT        NOT NULL);''')
        print("AD_REQUEST Record table created successfully")

        self.conn.execute('''CREATE TABLE FOLLOWERS
                        (UID            INTEGER     NOT NULL,
                         FID             INTEGER     NOT NULL,
                         CONSTRAINT uid_fid_unique UNIQUE (UID, FID)
                        );''')
        print("FOLLOWERS Record table created successfully")

    # Quarry
    def QueryAllCampaigns(self):
        try:
            query = """SELECT CID, SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged
                    FROM CAMPAIGN;"""
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryRecentCampaigns(self):
        try:
            query = """SELECT CID, SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged
                    FROM CAMPAIGN
                    ORDER BY SDate DESC
                    LIMIT 6;"""
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()
        
    def QueryCampaignByCID(self, CID):
        try:
            query = """SELECT CID, SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged
                    FROM CAMPAIGN
                    where CID = {0};""".format(CID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryCampaignBySID(self, SID):
        try:
            query = """SELECT CID, SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged
                    FROM CAMPAIGN
                    where SID = {0};""".format(SID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryCampaignIDAndNameAndBudgetBySID(self, SID):
        try:
            query = """SELECT CID, Title, Budget
                    FROM CAMPAIGN
                    where SID = {0} and Flagged = 'NO';""".format(SID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()
    
    def QueryPublicCampaign(self):
        try:
            query = """SELECT CID, SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged
                    FROM CAMPAIGN
                    where visibility = 'Public' and Flagged = 'NO';"""
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QuerySponsorInBoxChatOverView(self, SID):
        try:
            query = """SELECT AID, CID, SID, IID, REQUEST_FROM, STATUS, TIMESTAMP, MSG, Budget_nig, TERMS_nig, SEEN_SOPN, SEEN_INFL
                        FROM AD_REQUEST
                        WHERE (SID, timestamp) IN (
                            SELECT SID, MAX(timestamp)
                            FROM AD_REQUEST
                            WHERE SID = '{0}'
                            GROUP BY IID
                        )
                        ORDER BY TIMESTAMP DESC;
                        """.format(SID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryInfluencerInBoxChatOverView(self, IID):
        try:
            query = """SELECT AID, CID, SID, IID, REQUEST_FROM, STATUS, TIMESTAMP, MSG, Budget_nig, TERMS_nig, SEEN_SOPN, SEEN_INFL
                        FROM AD_REQUEST
                        WHERE (IID, timestamp) IN (
                            SELECT IID, MAX(timestamp)
                            FROM AD_REQUEST
                            WHERE IID = '{0}'
                            GROUP BY SID
                        )
                        ORDER BY TIMESTAMP DESC;
                        """.format(IID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()


    def QuerySponsorInBoxChat(self, SID, IID):
        try:
            query = """SELECT AID, CID, SID, IID, REQUEST_FROM, STATUS, TIMESTAMP, MSG, Budget_nig, TERMS_nig, SEEN_SOPN, SEEN_INFL
                        FROM AD_REQUEST
                        WHERE SID = '{0}' and IID = '{1}'
                        ORDER BY TIMESTAMP DESC;""".format(SID, IID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryInfluencerInBoxChat(self, IID, SID):
        try:
            query = """SELECT AID, CID, SID, IID, REQUEST_FROM, STATUS, TIMESTAMP, MSG, Budget_nig, TERMS_nig, SEEN_SOPN, SEEN_INFL
                        FROM AD_REQUEST
                        WHERE SID = '{0}' and IID = '{1}'
                        ORDER BY TIMESTAMP DESC;""".format(SID, IID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QuerySponsorInBoxChatLastBudget(self, IID, SID, CID):
        try:
            query = """SELECT Budget_nig
                        FROM AD_REQUEST
                        WHERE SID = '{0}' and IID = '{1}' and CID = '{2}'
                        ORDER BY TIMESTAMP DESC;""".format(SID, IID, CID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QuerySponsorInBoxChatLastTerm(self, IID, SID, CID):
        try:
            query = """SELECT TERMS_nig
                        FROM AD_REQUEST
                        WHERE SID = '{0}' and IID = '{1}' and CID = '{2}'
                        ORDER BY TIMESTAMP DESC;""".format(SID, IID, CID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryInfluencerInBoxChatLastBudget(self, IID, SID, CID):
        try:
            query = """SELECT Budget_nig
                        FROM AD_REQUEST
                        WHERE SID = '{0}' and IID = '{1}' and CID = '{2}'
                        ORDER BY TIMESTAMP DESC;""".format(SID, IID, CID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryInfluencerInBoxChatLastTerm(self, IID, SID, CID):
        try:
            query = """SELECT TERMS_nig
                        FROM AD_REQUEST
                        WHERE SID = '{0}' and IID = '{1}' and CID = '{2}'
                        ORDER BY TIMESTAMP DESC;""".format(SID, IID, CID)
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    def QueryFollowers(self, UID):
        try:
            query = """SELECT UID, FID
                        FROM FOLLOWERS
                        WHERE UID = '{0}';""".format(UID)
            result = self.SqlQuarryExec(query)
            if result == []:
                return [[],[]]
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()
            return [[],[]]
        
    def QueryFlaggedCampaignsStats(self):
        try:
            query = """
            SELECT
              SUM(CASE WHEN Flagged = 'YES' THEN 1 ELSE 0 END) AS flagged_count,
              SUM(CASE WHEN Flagged = 'NO' THEN 1 ELSE 0 END) AS non_flagged_count
            FROM CAMPAIGN;
            """
            result = self.SqlQuarryExec(query)
            # Assuming result is a list of tuples, with the first tuple containing the counts
            flagged_count, non_flagged_count = result[0]
            return flagged_count, non_flagged_count
        except Exception as e:
            print(e)
            self.conn.rollback()
            return 0, 0
        
    def QueryCampaignsVisibilityStats(self):
        try:
            query = """
            SELECT
              SUM(CASE WHEN Visibility = 'Public' THEN 1 ELSE 0 END) AS public_count,
              SUM(CASE WHEN Visibility = 'Private' THEN 1 ELSE 0 END) AS private_count
            FROM CAMPAIGN;
            """
            result = self.SqlQuarryExec(query)
            # Assuming result is a list of tuples, with the first tuple containing the counts
            public_count, private_count = result[0]
            return public_count, private_count
        except Exception as e:
            print(e)
            self.conn.rollback()
            return 0, 0
        
    def QueryCampaignsAcceptanceStatus(self):
        try:
            query = """
                SELECT 
                    SUM(CASE WHEN subquery.STATUS = 'Approved' THEN 1 ELSE 0 END) AS accepted_count,
                    SUM(CASE WHEN subquery.STATUS = 'Rejected' THEN 1 ELSE 0 END) AS rejected_count,
                    SUM(CASE WHEN subquery.STATUS = 'PENDING' THEN 1 ELSE 0 END) AS pending_count
                FROM 
                    (SELECT 
                        IID, 
                        CID, 
                        STATUS, 
                        MAX(TIMESTAMP) AS TIMESTAMP
                    FROM 
                        AD_REQUEST 
                    GROUP BY 
                        IID, CID, STATUS
                    ) AS subquery;"""
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]

        except Exception as e:
            print(e, "error")
            self.conn.rollback()
            return []
    
    def QueryCampaignTitleID(self):
        try:
            query = """SELECT CID, Title
                    FROM CAMPAIGN;"""
            result = self.SqlQuarryExec(query)
            return [list(column) for column in zip(*result)]
        except Exception as e:
            print(e)
            self.conn.rollback()

    # add
    def AddCampaigns(self, SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged):
        try:
            c = self.conn.cursor()
            c.execute("""INSERT INTO CAMPAIGN (SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged) VALUES 
                    ({0}, \"{1}\", \"{2}\", {3}, {4}, {5}, \"{6}\", \"{7}\", \"{8}\")""".format(
                SID, Title, Description, SDate, EDate, Budget, Visibility, Goal, Flagged))

            self.Commit()
            return True, c.lastrowid
        except Exception as e:
            self.conn.rollback()
            return False, 0
    
    def AddAdRequest(self, CID, SID, IID, REQUEST_FROM, STATUS, MSG, Budget, Terms, SEEN_SOPN, SEEN_INFL):
        try:
            c = self.conn.cursor()
            c.execute("""INSERT INTO AD_REQUEST (CID, SID, IID, REQUEST_FROM, STATUS, TIMESTAMP, MSG, Budget_nig, TERMS_nig, SEEN_SOPN, SEEN_INFL) VALUES 
                    ({0}, {1}, {2}, \"{3}\", \"{4}\", {5}, \"{6}\", \"{7}\", \"{8}\", \"{9}\", \"{10}\")""".format(
                CID, SID, IID, REQUEST_FROM, STATUS, int(time.time()), MSG, Budget, Terms, SEEN_SOPN, SEEN_INFL))
            self.Commit()
            return True, c.lastrowid
        except Exception as e:
            self.conn.rollback()
            return False, 0
        
    def AddFollower(self, UID, FID):
        try:
            c = self.conn.cursor()
            c.execute("""INSERT INTO FOLLOWERS (UID, FID) VALUES 
                    ({0}, {1})""".format(UID, FID))
            self.Commit()
            return True, c.lastrowid
        except Exception as e:
            self.conn.rollback()
            return False, 0

    # remove
    def RemoveACCESSByUID(self, UID):
        try:
            self.conn.execute(
                "DELETE from ACCESS where UID={0}".format(UID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
        
    def RemoveSponsorCampaigns(self, SID):
        try:
            self.conn.execute(
                "DELETE from CAMPAIGN where SID={0}".format(SID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
    
    def RemoveInfluencerAdRequest(self, IID):
        try:
            self.conn.execute(
                "DELETE from AD_REQUEST where IID={0}".format(IID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
    
    def RemoveSponsorAdRequest(self, SID):
        try:
            self.conn.execute(
                "DELETE from AD_REQUEST where SID={0}".format(SID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
        
    def RemoveCampaign(self, CID):
        try:
            self.conn.execute(
                "DELETE from CAMPAIGN where CID={0}".format(CID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
        
    def RemoveChat(self, IID, SID):
        try:
            self.conn.execute(
                "DELETE from AD_REQUEST where IID={0} and SID={1}".format(IID, SID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
    
    def RemoveFollower(self, UID, FID):
        try:
            self.conn.execute(
                "DELETE from FOLLOWERS where UID={0} and FID={1}".format(UID, FID))
            self.Commit()
            return True
        except Exception as exc:
            print(exc)
            self.conn.rollback()
            return False


    # update
    
    def flagCampaign(self, CID):
        try:
            self.conn.execute(
                "UPDATE CAMPAIGN set Flagged = \"YES\" where CID = {0}".format(CID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
        
    def unflagCampaign(self, CID):
        try:
            self.conn.execute(
                "UPDATE CAMPAIGN set Flagged = \"NO\" where CID = {0}".format(CID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
    
    def updateAdRequestStatus(self, IID, SID, status, CID):
        try:
            self.conn.execute(
                "UPDATE AD_REQUEST set STATUS = \"{0}\" where IID = {1} and SID = {2} and CID = {3}".format(status, IID, SID, CID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
        
    def updateAdRequestSeenSOPN(self, IID, SID):
        try:
            self.conn.execute(
                "UPDATE AD_REQUEST set SEEN_SOPN = \"True\" where IID = {0} and SID = {1}".format(IID, SID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
    
    def updateAdRequestSeenINFL(self, IID, SID):
        try:
            self.conn.execute(
                "UPDATE AD_REQUEST set SEEN_INFL = \"True\" where IID = {0} and SID = {1}".format(IID, SID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
        
    def SetCampaignVisibility(self, CID, visibility):
        try:
            self.conn.execute(
                "UPDATE CAMPAIGN set Visibility = \"{0}\" where CID = {1}".format(visibility, CID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
        
    def UpdateCampaigns(self, CID, Title, Description, SDate, EDate, Budget, Visibility, Goal):
        try:
            self.conn.execute(
                "UPDATE CAMPAIGN set Title = \"{0}\", Description = \"{1}\", SDate = {2}, EDate = {3}, Budget = {4}, Visibility = \"{5}\", Goal = \"{6}\" where CID = {7}".format(Title, Description, SDate, EDate, Budget, Visibility, Goal, CID))
            self.Commit()
            return True
        except:
            self.conn.rollback()
            return False
    # Misc
    def SqlQuarryExec(self, quarry):
        c = self.conn.cursor()
        c.execute(quarry)
        return (c.fetchall())

    def Commit(self):
        self.conn.commit()


if __name__ == "__main__":
    db = DB_Manager()
    # db.TableCreation()
