#!/usr/bin/env ruby
require "rqrcode"

qrcode = RQRCode::QRCode.new("https://praecipula.github.io/l/example")

# NOTE: showing with default options specified explicitly
svg = qrcode.as_svg(
  color: "000",
  shape_rendering: "crispEdges",
  module_size: 11,
  standalone: true,
  use_path: true
)

puts svg
