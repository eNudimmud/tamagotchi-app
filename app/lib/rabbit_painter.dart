import 'package:flutter/material.dart';
import 'models.dart';

/// Dessine le lapin E*NKI en vectoriel (CustomPainter).
/// Spec visuel (SOUL.md) : lapin humanoide blanc, grandes oreilles, yeux
/// heterochrones (gauche rouge/orange #E8521F, droite jaune/or #F4C430),
/// jaquette moutarde #E8B800 avec logo "iii" blanc dans le dos, hoodie rouge
/// #C0392B, cargo vert #4B5320, baskets violettes #6B3FA0.
///
/// `t` (0..1) pilote le cycle de respiration/animation. `mood` module
/// l'expression (yeux, bouche). `facingBack` bascule sur la vue dos (logo iii).

class RabbitPainter extends CustomPainter {
  final double t;
  final Mood mood;
  final bool facingBack;
  final double blink;

  RabbitPainter({
    required this.t,
    required this.mood,
    this.facingBack = false,
    this.blink = 1.0,
  });

  static const _white = Color(0xFFF7F7F2);
  static const _earInner = Color(0xFFF2C9C9);
  static const _eyeL = Color(0xFFE8521F);
  static const _eyeR = Color(0xFFF4C430);
  static const _jacket = Color(0xFFE8B800);
  static const _hoodie = Color(0xFFC0392B);
  static const _cargo = Color(0xFF4B5320);
  static const _sneaker = Color(0xFF6B3FA0);

  @override
  void paint(Canvas canvas, Size size) {
    final cx = size.width / 2;
    final breath = (0.5 - 0.5 * (1 - (t % 1))).abs();
    final bob = breath * 4.0;
    final c = canvas;
    c.translate(0, -bob);

    if (facingBack) {
      _paintBack(c, size, cx);
      return;
    }

    // --- oreilles ---
    final earSwing = (t % 1) * 0.12 - 0.06;
    _ear(c, cx - 22, size.height * 0.12, -earSwing);
    _ear(c, cx + 22, size.height * 0.12, earSwing);

    // --- tete ---
    final headY = size.height * 0.30;
    final headR = size.width * 0.17;
    final head = Offset(cx, headY);
    c.drawCircle(head, headR, Paint()..color = _white);

    // yeux heterochrones
    final eyeY = headY - headR * 0.05;
    final eyeDx = headR * 0.45;
    _eye(c, Offset(head.dx - eyeDx, eyeY), _eyeL, blink);
    _eye(c, Offset(head.dx + eyeDx, eyeY), _eyeR, blink);

    // bouche selon humeur
    _mouth(c, head.dx, headY + headR * 0.45, headR * 0.4, mood.state);

    // --- corps (hoodie rouge + jaquette moutarde) ---
    final bodyTop = headY + headR * 0.9;
    final bodyW = size.width * 0.42;
    final bodyH = size.height * 0.34;
    final body = RRect.fromRectAndRadius(
      Rect.fromCenter(
        center: Offset(cx, bodyTop + bodyH / 2),
        width: bodyW,
        height: bodyH,
      ),
      const Radius.circular(26),
    );
    c.drawRRect(body, Paint()..color = _hoodie);
    // jaquette moutarde par-dessus (rivette)
    final jacket = RRect.fromRectAndRadius(
      Rect.fromCenter(
        center: Offset(cx, bodyTop + bodyH * 0.62),
        width: bodyW * 0.7,
        height: bodyH * 0.62,
      ),
      const Radius.circular(18),
    );
    c.drawRRect(jacket, Paint()..color = _jacket);

    // bras
    _arm(c, cx - bodyW * 0.5, bodyTop + bodyH * 0.35, -0.2);
    _arm(c, cx + bodyW * 0.5, bodyTop + bodyH * 0.35, 0.2);

    // --- jambes cargo + baskets ---
    final legTop = bodyTop + bodyH;
    _leg(c, cx - bodyW * 0.22, legTop, cargo: _cargo, sneaker: _sneaker);
    _leg(c, cx + bodyW * 0.22, legTop, cargo: _cargo, sneaker: _sneaker);
  }

  void _ear(Canvas c, double x, double topY, double tilt) {
    c.save();
    c.translate(x, topY + 60);
    c.rotate(tilt);
    final p = Path();
    p.moveTo(-16, 60);
    p.quadraticBezierTo(-30, -10, 0, -70);
    p.quadraticBezierTo(30, -10, 16, 60);
    p.close();
    c.drawPath(p, Paint()..color = _white);
    final inr = Path();
    inr.moveTo(-7, 50);
    inr.quadraticBezierTo(-12, 0, 0, -50);
    inr.quadraticBezierTo(12, 0, 7, 50);
    inr.close();
    c.drawPath(inr, Paint()..color = _earInner);
    c.restore();
  }

  void _eye(Canvas c, Offset o, Color col, double blink) {
    final r = 7.0;
    if (blink < 0.3) {
      c.drawLine(
        Offset(o.dx - r, o.dy),
        Offset(o.dx + r, o.dy),
        Paint()
          ..color = const Color(0xFF333333)
          ..strokeWidth = 2,
      );
      return;
    }
    c.drawCircle(o, r, Paint()..color = col);
    c.drawCircle(o, r, Paint()..color = const Color(0x55000000)..style = PaintingStyle.stroke..strokeWidth = 1.5);
    c.drawCircle(Offset(o.dx - 2, o.dy - 2), 2, Paint()..color = Colors.white);
  }

  void _mouth(Canvas c, double x, double y, double w, String moodState) {
    final paint = Paint()
      ..color = const Color(0xFF333333)
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;
    final p = Path();
    if (moodState == 'happy') {
      p.moveTo(x - w, y);
      p.quadraticBezierTo(x, y + w * 1.1, x + w, y);
    } else if (moodState == 'sad' || moodState == 'sick') {
      p.moveTo(x - w, y + w * 0.6);
      p.quadraticBezierTo(x, y - w * 0.2, x + w, y + w * 0.6);
    } else if (moodState == 'hungry' || moodState == 'sleepy') {
      p.moveTo(x - w * 0.6, y);
      p.lineTo(x + w * 0.6, y);
    } else {
      p.moveTo(x - w * 0.5, y);
      p.quadraticBezierTo(x, y + w * 0.5, x + w * 0.5, y);
    }
    c.drawPath(p, paint);
  }

  void _arm(Canvas c, double x, double y, double dir) {
    c.save();
    c.translate(x, y);
    c.rotate(dir);
    final p = RRect.fromRectAndRadius(
      Rect.fromCenter(center: Offset(0, 18), width: 18, height: 44),
      const Radius.circular(9),
    );
    c.drawRRect(p, Paint()..color = _hoodie);
    c.restore();
  }

  void _leg(Canvas c, double x, double top, {required Color cargo, required Color sneaker}) {
    final p = RRect.fromRectAndRadius(
      Rect.fromCenter(center: Offset(x, top + 26), width: 24, height: 52),
      const Radius.circular(8),
    );
    c.drawRRect(p, Paint()..color = cargo);
    c.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(center: Offset(x, top + 54), width: 32, height: 16),
        const Radius.circular(8),
      ),
      Paint()..color = sneaker,
    );
  }

  void _paintBack(Canvas c, Size size, double cx) {
    final headY = size.height * 0.30;
    final headR = size.width * 0.17;
    c.drawCircle(Offset(cx, headY), headR, Paint()..color = _white);
    _ear(c, cx - 22, size.height * 0.12, -0.06);
    _ear(c, cx + 22, size.height * 0.12, 0.06);
    final bodyTop = headY + headR * 0.9;
    final bodyW = size.width * 0.42;
    final bodyH = size.height * 0.34;
    final body = RRect.fromRectAndRadius(
      Rect.fromCenter(
        center: Offset(cx, bodyTop + bodyH / 2),
        width: bodyW,
        height: bodyH,
      ),
      const Radius.circular(26),
    );
    c.drawRRect(body, Paint()..color = _hoodie);
    // logo iii blanc
    final jcx = cx;
    final jcy = bodyTop + bodyH * 0.55;
    final lp = Paint()..color = Colors.white;
    for (final dx in const [-12.0, 0.0, 12.0]) {
      c.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromCenter(center: Offset(jcx + dx, jcy), width: 5, height: 26),
          const Radius.circular(2.5),
        ),
        lp,
      );
    }
  }

  @override
  bool shouldRepaint(covariant RabbitPainter old) =>
      old.t != t || old.mood.state != mood.state || old.facingBack != facingBack || old.blink != blink;
}

/// Petit helper d'animation : clignement aleatoire base sur le temps.
double blinkFor(DateTime now) {
  final sec = now.second + now.millisecond / 1000;
  // clignement court toutes les ~4s
  final phase = sec % 4.0;
  if (phase < 0.12) return 0.0;
  if (phase < 0.24) return 1.0;
  return 1.0;
}
