from __future__ import annotations
import re
import requests
from typing import Dict, List, Optional

MANIFEST_LOCATION = "https://launchermeta.mojang.com/mc/game/version_manifest.json"	 # noqa: E501
EARLIEST_SUPPORTED_VERSION_ID = '19w36a'


class VersionError(Exception):
	pass


class NoSuchVersionError(VersionError):
	pass


class Version:
	def __init__(
		self,
		id: str,
		index: int,
		next: Optional[Version] = None
	) -> None:

		self.id = id
		self._index = index
		self.next = next

	def __str__(self) -> str:
		return self.id

	def __lt__(self, other) -> bool:
		if not isinstance(other, Version):
			return False

		return self._index < other._index

	def __gt__(self, other) -> bool:
		if not isinstance(other, Version):
			return False

		return self._index > other._index

	def to(self, other: Optional[Version], snapshots=True) -> List[Version]:
		"""Iterate over all the versions from this version (inclusive) to
		`other` (exclusive)

		Args:
			other (Optional[Version]): Stop before reaching this version
			include_snapshots (bool, optional): Defaults to True.

		Returns:
			List[Version]: All the versions since this version, before `other`
		"""

		if other < self:
			dots = '...' if snapshots else '..'
			raise ValueError(
				'Version B cannot have been released sooner than version A in'
				+ f' A{dots}B syntax'
			)

		r = []
		curr = self
		while curr is not None and (other is None or curr != other.next):
			if snapshots or isinstance(curr, Release):
				r.append(curr)

			curr = curr.next

		return r

	@staticmethod
	def parse(raw: Dict, index: int) -> Version:
		id = raw['id']
		type_ = raw['type']

		if type_ == 'snapshot':
			return Snapshot(id, index)
		elif type_ == 'release':
			return Release(id, index)
		elif type_ == 'old_alpha':
			return OldAlphaVersion(id, index)
		elif type_ == 'old_beta':
			return OldBetaVersion(id, index)
		else:
			raise Exception(f'Unknown version type: {type_}')

	@staticmethod
	def of(id: Optional[str]) -> Version:
		if id is None:
			return manifest.latest_snapshot

		if id not in manifest.version_for_id:
			raise NoSuchVersionError(f"Unsupported Minecraft version '{id}'")

		return manifest.version_for_id[id]

	@staticmethod
	def pattern(p: str) -> List[Version]:
		# First, check if the pattern is a range
		m = re.match(r'(.*[^.])?(\.\.\.?)(.*)', p)
		if m is not None:
			a_id, dots, b_id = m.groups()
			snapshots = dots == '...'

			if a_id:
				a = Version.of(a_id)
			else:
				# Get the earliest release or snapshot to start at
				a = manifest.earliest_snapshot if snapshots else manifest.earliest_release

			if b_id:
				b = Version.of(b_id)
			else:
				# Get all the commits since `a`
				b = None

			return a.to(b, snapshots)

		else:
			# Then, try to treat it as a version
			return [Version.of(p)]

	@staticmethod
	def patterns(patterns: List[str]) -> List[Version]:
		# Parse versions
		versions = set()
		for pattern in patterns:
			if pattern.startswith('-'):
				versions -= set(Version.pattern(pattern[1:]))
			else:
				versions |= set(Version.pattern(pattern))

		# Sort
		versions = list(versions)
		versions.sort()

		return versions


class Release(Version):
	@staticmethod
	def of(id: Optional[str]) -> Release:
		if id is None:
			return manifest.latest_release

		else:
			version = Version.of(id)
			if not isinstance(version, Release):
				raise ValueError('Version is not a release')

			return version


class Snapshot(Version):
	pass


class OldVersion(Version):
	pass


class OldAlphaVersion(Version):
	pass


class OldBetaVersion(Version):
	pass


class Manifest:
	def __init__(
		self,
		versions: List[Version],
		earliest_release: Release,
		earliest_snapshot: Version,
		latest_release: Release,
		latest_snapshot: Version
	) -> None:

		self.versions = versions
		self.version_for_id = {version.id: version for version in versions}
		self.earliest_release = earliest_release
		self.earliest_snapshot = earliest_snapshot
		self.latest_release = latest_release
		self.latest_snapshot = latest_snapshot

	def __iter__(self) -> Version:
		return self.versions

	@staticmethod
	def parse(
		raw: Dict,
		earliest_supported_version_id: Optional[str]
	) -> Manifest:

		# Reverse to get ascending chronological order
		reversed_versions = reversed(raw['versions'])

		current_version_supported = False
		earliest_release = None
		earliest_snapshot = None
		versions = []
		version_for_id = {}
		prev = None

		for i, raw_version in enumerate(reversed_versions):
			id = raw_version['id']
			if id == earliest_supported_version_id:
				current_version_supported = True

			if not current_version_supported:
				continue

			version = Version.parse(raw_version, i)
			versions.append(version)
			version_for_id[id] = version

			if prev is not None:
				prev.next = version
			prev = version

			if earliest_snapshot is None:
				earliest_snapshot = version
			if earliest_release is None and isinstance(version, Release):
				earliest_release = version

		latest_release = version_for_id[raw['latest']['release']]
		latest_snapshot = version_for_id[raw['latest']['snapshot']]

		return Manifest(
			versions,
			earliest_release,
			earliest_snapshot,
			latest_release,
			latest_snapshot
		)


def load_manifest(
	raw: Optional[Dict] = None,
	earliest_supported_version_id: Optional[str] = EARLIEST_SUPPORTED_VERSION_ID
):

	global manifest

	if raw is None:
		raw = requests.get(MANIFEST_LOCATION).json()
	manifest = Manifest.parse(raw, earliest_supported_version_id)


manifest = None
