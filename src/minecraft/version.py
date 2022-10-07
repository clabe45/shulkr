from __future__ import annotations
import re
import requests
from typing import Dict, List, Optional

MANIFEST_LOCATION = "https://launchermeta.mojang.com/mc/game/version_manifest.json"	 # noqa: E501
EARLIEST_SUPPORTED_VERSION_ID = '19w36a'


class VersionError(Exception):
	"""Base class for all exceptions raised by this module."""


class NoSuchVersionError(VersionError):
	"""Raised when a version is not supported by this module."""


class Version:
	"""Represents a Minecraft version.

	Attributes:
		id (str): The version ID.
		_index (int): The index of this version in the manifest.
		next (Optional[Version]): The next version, or None if this is the
			latest version.
	"""

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
		"""Parse a version from a dictionary.

		Args:
			raw (Dict): The dictionary to parse.
			index (int): The index of this version in the manifest.

		Returns:
			Version: The parsed version.
		"""

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
		"""Get a version by its ID.

		Args:
			id (Optional[str]): The ID of the version to get.

		Returns:
			Version: The version with the given ID.

		Raises:
			NoSuchVersionError: If the version is not supported.
		"""

		if id is None:
			return manifest.latest_snapshot

		if id not in manifest.version_for_id:
			raise NoSuchVersionError(f"Unsupported Minecraft version '{id}'")

		return manifest.version_for_id[id]

	@staticmethod
	def pattern(p: str, latest_in_repo: Version = None) -> List[Version]:
		"""Parse a version pattern.

		Args:
			p (str): The pattern to parse.
			latest_in_repo (Version, optional): The latest version in the
				repository. Defaults to None.

		Returns:
			List[Version]: The versions matching the pattern.

		Raises:
			ValueError: If the pattern is invalid.
		"""

		# First, check if the pattern is a range
		m = re.match(r'(.*[^.])?(\.\.\.?)(.*)', p)
		if m is not None:
			a_id, dots, b_id = m.groups()
			snapshots = dots == '...'

			if a_id:
				a = Version.of(a_id)
			else:
				# Get the next version after the latest committed one
				if latest_in_repo:
					a = latest_in_repo.next
					if not snapshots:
						# Find the next release
						while a is not None and not isinstance(a, Release):
							a = a.next
				else:
					raise ValueError('No commits from which to derive current version')

			if a is None:
				# No more versions or releases to generate
				return []

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
	def patterns(
		patterns: List[str],
		latest_in_repo: Version = None
	) -> List[Version]:
		"""Parse a list of version patterns.

		Args:
			patterns (List[str]): The patterns to parse.
			latest_in_repo (Version, optional): The latest version in the
				repository. Defaults to None.

		Returns:
			List[Version]: The versions matching the patterns.

		Raises:
			ValueError: If a pattern is invalid.
		"""

		# Parse versions
		versions = set()
		for pattern in patterns:
			if pattern.startswith('-'):
				versions -= set(Version.pattern(pattern[1:], latest_in_repo))
			else:
				versions |= set(Version.pattern(pattern, latest_in_repo))

		# Sort
		versions = list(versions)
		versions.sort()

		return versions


class Release(Version):
	"""Represents a Minecraft release.

	Attributes:
		id (str): The version ID.
		_index (int): The index of this version in the manifest.
		next (Optional[Version]): The next version, or None if this is the
			latest version.
	"""

	@staticmethod
	def of(id: Optional[str]) -> Release:
		"""Get a release by its ID.

		Args:
			id (Optional[str]): The ID of the release to get.

		Returns:
			Release: The release with the given ID.

		Raises:
			ValueError: If the version is not a release.
		"""

		if id is None:
			return manifest.latest_release

		else:
			version = Version.of(id)
			if not isinstance(version, Release):
				raise ValueError('Version is not a release')

			return version


class Snapshot(Version):
	"""Represents a Minecraft snapshot.

	Attributes:
		id (str): The version ID.
		_index (int): The index of this version in the manifest.
		next (Optional[Version]): The next version, or None if this is the
			latest version.
	"""


class OldVersion(Version):
	"""Represents an old Minecraft version.

	Attributes:
		id (str): The version ID.
		_index (int): The index of this version in the manifest.
		next (Optional[Version]): The next version, or None if this is the
			latest version.
	"""


class OldAlphaVersion(Version):
	"""Represents an old Minecraft alpha version.

	Attributes:
		id (str): The version ID.
		_index (int): The index of this version in the manifest.
		next (Optional[Version]): The next version, or None if this is the
			latest version.
	"""


class OldBetaVersion(Version):
	"""Represents an old Minecraft beta version.

	Attributes:
		id (str): The version ID.
		_index (int): The index of this version in the manifest.
		next (Optional[Version]): The next version, or None if this is the
			latest version.
	"""


class Manifest:
	"""Represents the Minecraft version manifest.

	Attributes:
		versions (List[Version]): All the versions in the manifest.
		version_for_id (Dict[str, Version]): A mapping from version IDs to
			versions.
		earliest_release (Release): The earliest release in the manifest.
		earliest_snapshot (Version): The earliest snapshot in the manifest.
		latest_release (Release): The latest release in the manifest.
		latest_snapshot (Version): The latest snapshot in the manifest.
	"""

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
		"""Parse a manifest from a dictionary.

		Args:
			raw (Dict): The dictionary to parse.
			earliest_supported_version_id (Optional[str]): The earliest
				supported version ID.

		Returns:
			Manifest: The parsed manifest.
		"""

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
	"""Load the Minecraft version manifest.

	Args:
		raw (Optional[Dict], optional): The manifest to load. Defaults to None.
		earliest_supported_version_id (Optional[str], optional): The earliest
			supported version ID. Defaults to EARLIEST_SUPPORTED_VERSION_ID.
	"""

	global manifest

	if raw is None:
		raw = requests.get(MANIFEST_LOCATION).json()
	manifest = Manifest.parse(raw, earliest_supported_version_id)


def clear_manifest():
	"""Clear the loaded Minecraft version manifest."""

	global manifest

	manifest = None
