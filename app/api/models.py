from datetime import datetime

from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey

# モデルのベースクラスを定義
from sqlalchemy.orm.decl_api import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users" # テーブル名
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True, nullable=False)
    email = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True, nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # machine_informationsテーブルとの一対多のリレーション
    machine_informations = relationship(
        "MachineInformation", # リレーション先モデル名
        back_populates="user", # リレーション先での変数名
        cascade="all, delete-orphan",# "all, delete-orphan": userを削除したときに、関連する items を削除する
    )

    # batting_centersテーブルとの多対多のリレーション
    itta_centers = relationship(
        "BattingCenter", # リレーション先モデル名
        secondary="itta_users_centers", # 中間テーブル
        back_populates="itta_users", # リレーション先での変数名
    )

    # machine_informationsテーブルとの多対多のリレーション（中間テーブル：atta_users_machines）
    atta_machines = relationship("MachineInformation", secondary="atta_users_machines", back_populates="atta_users")

    # machine_informationsテーブルとの多対多のリレーション（中間テーブル：nakatta_users_machines）
    nakatta_machines = relationship("MachineInformation", secondary="nakatta_users_machines", back_populates="nakatta_users")


class BattingCenter(Base):
    __tablename__ = "batting_centers"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # machine_informationsテーブルとの一対多のリレーション
    machine_informations = relationship("MachineInformation", back_populates="batting_center", cascade="all, delete-orphan")

    # usersテーブルとの多対多のリレーション
    itta_users = relationship("User", secondary="itta_users_centers", back_populates="itta_centers")

    def set_itta_flag(self, user: User) -> str:
        if self in user.itta_centers:
            return "yes"
        else:
            return "no"

    def count_itta(self) -> int:
        return len(self.itta_users)


class IttaUsersCenters(Base):
    """usersとbatting_centersの中間テーブル"""
    __tablename__ = "itta_users_centers"
    __table_args__ = (
        UniqueConstraint("user_id", "batting_center_id", name="unique_idx_userid_battingcenterid"),
        {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    batting_center_id = Column(Integer, ForeignKey("batting_centers.id"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class BreakingBall(Base):
    "球種を格納するテーブル"
    __tablename__ = "breaking_balls"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255, collation="utf8mb4_bin"), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class BallSpeed(Base):
    "球速の値一覧を格納するテーブル"
    __tablename__ = "ball_speeds"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    speed = Column(Integer, unique=True, nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class MachineInformation(Base):
    __tablename__ = "machine_informations"
    __table_args__ = (
        CheckConstraint("batter_box IN ('右', '左', '両')"),
        {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    batting_center_id = Column(Integer, ForeignKey("batting_centers.id"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # batter_boxに登録する値は、'右', '左', '両'に制限する
    batter_box = Column(String(255, collation="utf8mb4_bin"), nullable=False)

    # usersテーブルとのリレーション
    user = relationship("User", back_populates="machine_informations")

    # batting_centersテーブルとのリレーション
    batting_center = relationship("BattingCenter", back_populates="machine_informations")

    # beeaking_ballsテーブルとの多対多のリレーション（中間テーブル：machines_breaking_balls）
    beeaking_balls = relationship("BreakingBall", secondary="machines_breaking_balls")

    # ball_speedsテーブルとの多対多のリレーション（中間テーブル：machines_breaking_balls）
    ball_speeds = relationship("BallSpeed", secondary="machines_ball_speeds")

    # usersテーブルとの多対多のリレーション（中間テーブル：atta_users_machines）
    atta_users = relationship("User", secondary="atta_users_machines", back_populates="atta_machines")

    # usersテーブルとの多対多のリレーション（中間テーブル：nakatta_users_machines）
    nakatta_users = relationship("User", secondary="nakatta_users_machines", back_populates="nakatta_machines")


class MachineBreakingBall(Base):
    """machine_informationsとbreaking_ballsの中間テーブル"""
    __tablename__ = "machines_breaking_balls"
    __table_args__ = (
        UniqueConstraint("machine_id", "breaking_ball_id", name="unique_idx_machine_id_breaking_ball_id"),
        {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    )

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machine_informations.id"), nullable=False)
    breaking_ball_id = Column(Integer, ForeignKey("breaking_balls.id"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class MachineBallSpeed(Base):
    """machine_informationsとball_speedsの中間テーブル"""
    __tablename__ = "machines_ball_speeds"
    __table_args__ = (
        UniqueConstraint("machine_id", "ball_speed_id", name="unique_idx_machine_id_ball_speed_id"),
        {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    )

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machine_informations.id"), nullable=False)
    ball_speed_id = Column(Integer, ForeignKey("ball_speeds.id"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class AttaUserMachine(Base):
    """usersとmachine_informationsの中間テーブル（あった）"""
    __tablename__ = "atta_users_machines"
    __table_args__ = (
        UniqueConstraint("user_id", "machine_id", name="unique_idx_atta_userid_machineid"),
        {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machine_informations.id"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class NakattaUserMachine(Base):
    """usersとmachine_informationsの中間テーブル（なかった）"""
    __tablename__ = "nakatta_users_machines"
    __table_args__ = (
        UniqueConstraint("user_id", "machine_id", name="unique_idx_nakatta_userid_machineid"),
        {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machine_informations.id"), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
